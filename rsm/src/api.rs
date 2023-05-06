use axum::{extract::{State, Path}, Json};
use omnipaxos_core::{messages::Message, util::LogEntry};
use uuid::Uuid;
use reqwest::StatusCode;
use std::sync::Arc;
use serde::{Serialize, Deserialize};
use crate::{
    topology,
    consensus::OmnipaxosLogEntry,
    AppState,
};

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct OmnipaxosLogData {
   pub car_id: u64,
   pub from: u64,
   pub to: u64,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct ProposalRequest {
    pub data: OmnipaxosLogData,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct ReadRequest {
    pub from_idx: u64,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct ReadResponse {
    pub node_id: u64,
    pub decided_idx: u64,
    pub log_data: Vec<OmnipaxosLogEntry>,
}

pub async fn handle_apply(State(state): State<Arc<AppState>>, Json(req): Json<ProposalRequest>) -> StatusCode {
    println!("PID {}: Applying request from client", topology::get_pid());
    let msg = OmnipaxosLogEntry {
        id: (topology::get_pid(), Uuid::new_v4()),
        data: req.data,
    };
    match state.client_msg_queue_sender.send(msg).await {
        Ok(_) => StatusCode::OK,
        Err(_) => StatusCode::INTERNAL_SERVER_ERROR,
    }
}

pub async fn handle_omnipaxos(State(state): State<Arc<AppState>>, Json(msg): Json<Message<OmnipaxosLogEntry>>) -> StatusCode {
    match msg.clone() {
        Message::SequencePaxos(pm) => println!("PID {}: Paxos message from {}: {:?}", pm.to, pm.from, pm.msg),
        Message::BLE(_) => (),
    }
    match state.omnipaxos_incoming_sender.send(msg).await {
        Ok(_) => StatusCode::OK,
        Err(_) => StatusCode::INTERNAL_SERVER_ERROR,
    }
}

pub async fn handle_read(State(state): State<Arc<AppState>>, Path(from_idx): Path<u64>) -> Json<ReadResponse> {
    let op = state.omnipaxos.lock().unwrap();
    let decided_idx = op.get_decided_idx();
    if let Some(log) = op.read_decided_suffix(from_idx) {
        let log_data = log.iter().map(|entry| {
            match entry {
                LogEntry::Decided(cmd) => {
                    cmd.clone()
                }
                _ => {
                    panic!("something went wrong.") // TODO: maybe don't panic
                }
            }
        }).collect();
        Json(ReadResponse { node_id: topology::get_pid(), decided_idx, log_data })
    } else {
        Json(ReadResponse { node_id: topology::get_pid(), decided_idx, log_data: vec![] })
    }
}

pub async fn handle_print_log(State(state): State<Arc<AppState>>) -> StatusCode {
    println!("decided log: {:?}", state.omnipaxos.lock().unwrap().read_decided_suffix(0));
    StatusCode::OK
}