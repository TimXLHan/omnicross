use std::{env, net::SocketAddr, sync::{Arc, Mutex}};
use axum::{Router, routing::{put, post, get}, extract::{State, Json}};
use omnipaxos_storage::memory_storage::MemoryStorage;
use serde::{Serialize, Deserialize};
use omnipaxos_core::{messages::Message, omni_paxos::OmniPaxos};
use reqwest::StatusCode;
use consensus::{OmniPaxosServer, Command};
use tokio::sync::mpsc;
use uuid::Uuid;

mod util;
mod consensus;
mod topology;

#[macro_use]
extern crate lazy_static;

lazy_static! {
    static ref PORT: u16 = if let Ok(var) = env::var("PORT") {
        var.parse().unwrap()
    } else {
        8080
    };
}

struct AppState {
    omnipaxos_incoming_sender: mpsc::Sender<Message<Command>>,
    client_msg_queue_sender: mpsc::Sender<Command>,
    omnipaxos: Arc<Mutex<OmniPaxos<Command, MemoryStorage<Command>>>>,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct PutRequest {
    pub command: String,
}

async fn handle_apply(State(state): State<Arc<AppState>>, Json(req): Json<PutRequest>) -> StatusCode {
    let msg = Command {
        id: (topology::get_pid(), Uuid::new_v4()),
        command: req.command,
    };
    match state.client_msg_queue_sender.send(msg).await {
        Ok(_) => StatusCode::OK,
        Err(_) => StatusCode::INTERNAL_SERVER_ERROR,
    }
}

async fn handle_omnipaxos(State(state): State<Arc<AppState>>, Json(msg): Json<Message<Command>>) -> StatusCode {
    match state.omnipaxos_incoming_sender.send(msg).await {
        Ok(_) => StatusCode::OK,
        Err(_) => StatusCode::INTERNAL_SERVER_ERROR,
    }
}

async fn handle_print_log(State(state): State<Arc<AppState>>) -> StatusCode {
    println!("decided log: {:?}", state.omnipaxos.lock().unwrap().read_decided_suffix(0));
    StatusCode::OK
}

#[tokio::main]
async fn main() {
    let (omnipaxos_incoming_sender, omnipaxos_incoming_receiver) = mpsc::channel::<Message<Command>>(util::BUFFER_SIZE);
    let (client_msg_queue_sender, client_msg_queue_receiver) = mpsc::channel::<Command>(util::BUFFER_SIZE);

    let mut omnipaxosserver = OmniPaxosServer {
        omnipaxos: Arc::new(Mutex::new(consensus::build_omnipaxos_instance())),
        omnipaxos_incoming: omnipaxos_incoming_receiver,
        client_msg_queue: client_msg_queue_receiver,
        topology: topology::get_topology(),
    };

    let shared_state = Arc::new(AppState { 
        omnipaxos_incoming_sender,
        client_msg_queue_sender,
        omnipaxos: Arc::clone(&omnipaxosserver.omnipaxos),
    });

    tokio::spawn({
        // move omnipaxosserver into async tokio thread
        async move {
            omnipaxosserver.run().await;
        }
    });

    let router = Router::new()
        .route("/omnipaxos", post(handle_omnipaxos))
        .route("/apply",put(handle_apply))
        .route("/print_log", get(handle_print_log))
        .with_state(shared_state);

    let host = "0.0.0.0";
    println!("Starting server on {}:{}", host, *PORT);
    let addr: SocketAddr = format!("{}:{}", host, *PORT).parse().unwrap();
    axum::Server::bind(&addr)
        .serve(router.into_make_service())
        .await
        .unwrap()
}
