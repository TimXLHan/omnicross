use std::{env, net::SocketAddr, sync::{Arc, Mutex}};
use axum::{Router, routing::{put, post, get}};
use omnipaxos_storage::memory_storage::MemoryStorage;
use omnipaxos_core::{messages::Message, omni_paxos::OmniPaxos};
use consensus::{OmniPaxosServer, OmnipaxosLogEntry};
use tokio::sync::mpsc;

mod util;
mod consensus;
mod topology;
mod api;

#[macro_use]
extern crate lazy_static;

lazy_static! {
    static ref PORT: u16 = if let Ok(var) = env::var("PORT") {
        var.parse().unwrap()
    } else {
        8080
    };
}

pub struct AppState {
    omnipaxos_incoming_sender: mpsc::Sender<Message<OmnipaxosLogEntry>>,
    client_msg_queue_sender: mpsc::Sender<OmnipaxosLogEntry>,
    omnipaxos: Arc<Mutex<OmniPaxos<OmnipaxosLogEntry, MemoryStorage<OmnipaxosLogEntry>>>>,
}

#[tokio::main]
async fn main() {
    let (omnipaxos_incoming_sender, omnipaxos_incoming_receiver) = mpsc::channel::<Message<OmnipaxosLogEntry>>(util::BUFFER_SIZE);
    let (client_msg_queue_sender, client_msg_queue_receiver) = mpsc::channel::<OmnipaxosLogEntry>(util::BUFFER_SIZE);

    print!("Network topology for node {}", topology::get_pid());
    print!("{:?}", topology::get_topology());

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
        .route("/omnipaxos", post(api::handle_omnipaxos))
        .route("/apply",put(api::handle_apply))
        .route("/read/:from_idx", get(api::handle_read))
        .route("/print_log", get(api::handle_print_log))
        .with_state(shared_state);

    let host = "0.0.0.0";
    println!("Starting server on {}:{}", host, *PORT);
    let addr: SocketAddr = format!("{}:{}", host, *PORT).parse().unwrap();
    axum::Server::bind(&addr)
        .serve(router.into_make_service())
        .await
        .unwrap()
}
