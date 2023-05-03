use std::{env, collections::HashMap};
use omnipaxos_core::util::NodeId;

// Get configuration from environment.
lazy_static! {
    static ref PID: NodeId = if let Ok(var) = env::var("PID") {
        let x = var.parse().expect("PIDs must be u64");
        if x == 0 { panic!("PIDs cannot be 0") } else { x }
    } else {
        panic!("missing PID env var")
    };

    static ref PEERS: Vec<NodeId> = if let Ok(var) = env::var("PEERS") {
        var.split(",").map(|s| {
            let x = s.parse().expect("PIDs must be u64");
            if x == 0 { panic!("PIDs cannot be 0") } else { x }
        }).collect()
    } else {
        panic!("missing PEERS env var")
    };

    static ref PEER_ADDRS: Vec<String> = if let Ok(var) = env::var("PEER_ADDRS") {
        var.split(",").map(|x| x.to_owned()).collect()
    } else {
        panic!("missing PEERS env var")
    };
}

pub struct NodeInfo {
    pub addr: String,
    pub connected: bool,
}

pub type Topology = HashMap<NodeId, NodeInfo>;

pub fn get_pid() -> NodeId {
    *PID
}

pub fn get_peers() -> Vec<NodeId> {
    PEERS.clone()
}

pub fn get_topology() -> Topology {
    let mut topo: Topology = HashMap::default();
    for i in 0..PEERS.len() {
        topo.insert(PEERS[i], NodeInfo { addr: PEER_ADDRS[i].clone(), connected: false });
    };
    topo
}