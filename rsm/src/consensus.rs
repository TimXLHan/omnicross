use omnipaxos_core::{messages::Message, omni_paxos::{OmniPaxos, OmniPaxosConfig}, macros::Entry};
use omnipaxos_storage::memory_storage::MemoryStorage;
use serde::{Serialize, Deserialize};
use uuid::Uuid;
use std::{
    sync::{Arc, Mutex},
};
use crate::{
    util::{ELECTION_TIMEOUT, OUTGOING_MESSAGE_PERIOD},
    topology,
};
use tokio::{sync::mpsc, time};

pub fn build_omnipaxos_instance() -> OmniPaxos<Command, MemoryStorage<Command>> {
    let omnipaxos_config = OmniPaxosConfig {
        configuration_id: 1,
        pid: topology::get_pid(),
        peers: topology::get_peers(),
        ..Default::default()
    };
    
    let storage = MemoryStorage::<Command>::default();
    omnipaxos_config.build(storage)
}

#[derive(Clone, Debug, Serialize, Deserialize, Entry)]
pub struct Command {
    pub id: (u64, Uuid),
    pub command: String,
}

pub struct OmniPaxosServer {
    pub omnipaxos: Arc<Mutex<OmniPaxos<Command, MemoryStorage<Command>>>>,
    pub omnipaxos_incoming: mpsc::Receiver<Message<Command>>,
    pub client_msg_queue: mpsc::Receiver<Command>,
    pub topology: topology::Topology,
}

impl OmniPaxosServer {
    async fn send_outgoing_msgs(&mut self) {
        let omnipaxos_msgs = self.omnipaxos.lock().unwrap().outgoing_messages();
        for msg in omnipaxos_msgs {
            if let Some(receiver_node) = self.topology.get_mut(&msg.get_receiver()) { 
                let url = format!("http://{}/omnipaxos", receiver_node.addr);
                let result = reqwest::Client::new().post(url).json(&msg).send().await;
                match result {
                    Ok(_) => {
                        if !receiver_node.connected {
                            receiver_node.connected = true;
                        }
                    },
                    Err(_) => {
                        receiver_node.connected = false;
                    },
                }
            } else {
                panic!("Receiver not found in topology.")
            }
        }
    }

    pub(crate) async fn run(&mut self) {
        let mut outgoing_interval = time::interval(OUTGOING_MESSAGE_PERIOD);
        let mut election_interval = time::interval(ELECTION_TIMEOUT);
        loop {
            tokio::select! {
                biased;

                _ = election_interval.tick() => { self.omnipaxos.lock().unwrap().election_timeout(); },
                _ = outgoing_interval.tick() => { self.send_outgoing_msgs().await; },
                Some(incoming_msg) = self.omnipaxos_incoming.recv() => { self.omnipaxos.lock().unwrap().handle_incoming(incoming_msg); },
                Some(entry) = self.client_msg_queue.recv() => {
                    if let Err(_) = self.omnipaxos.lock().unwrap().append(entry) {
                        return (); // TODO: implement error handling
                    } 
                },
                else => { } 
            }
        }
    }
}