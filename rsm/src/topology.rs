use std::{env, collections::HashMap};
use omnipaxos_core::util::NodeId;

// Get configuration from environment.
lazy_static! {
    static ref RUNNING_IN_K8S_ENV: bool = if let Ok(var) = env::var("RUNNING_IN_K8S_ENV") {
        var.parse().expect("RUNNING_IN_K8S_ENV must be boolean")
    } else {
        panic!("not running in k8s environment")
    };

    static ref PORT: u16 = if let Ok(var) = env::var("PORT") {
        var.parse().unwrap()
    } else {
        8080
    };

    static ref PID: NodeId = if let Ok(var) = env::var("PODNAME") {
        let parts = var.split("-");
        let replica = parts.last().unwrap();
        let x: NodeId = replica.parse().expect("PIDs must be u64");
        let pid = x + 1; // replica numbers start with 0
        if pid == 0 { panic!("PIDs cannot be 0") } else { pid }
    } else {
        panic!("missing PID env var")
    };

    static ref NAMESPACE: String = if let Ok(var) = env::var("NAMESPACE") {
        var
    } else {
        panic!("missing NAMESPACE env var")
    };

    static ref SERVICENAME: String = if let Ok(var) = env::var("SERVICENAME") {
        var
    } else {
        panic!("missing SERVICENAME env var")
    };

    static ref STATEFULSETNAME: String = if let Ok(var) = env::var("STATEFULSETNAME") {
        var
    } else {
        panic!("missing STATEFULSETNAME env var")
    };

    static ref REPLICAS: u64 = if let Ok(var) = env::var("REPLICAS") {
        var.parse().expect("PIDs must be u64")
    } else {
        panic!("missing REPLICAS env var")
    };
}
#[derive(Debug, Clone)]
pub struct NodeInfo {
    pub addr: String,
    pub connected: bool,
}

pub type Topology = HashMap<NodeId, NodeInfo>;

pub fn get_pid() -> NodeId {
    *PID
}

pub fn get_peers() -> Vec<NodeId> {
    let mut peers: Vec<NodeId> = (1..*REPLICAS+1).collect(); // pid cannot be 0
    peers.retain(|&x| x != get_pid()); // remove own pid from peers
    peers
}

pub fn get_topology() -> Topology {
    let mut topo: Topology = HashMap::default();
    for peer in get_peers() {
        topo.insert(peer, NodeInfo { 
            addr: format!("{}-{}.{}.{}.svc.cluster.local:{}", *STATEFULSETNAME, peer-1, *SERVICENAME, *NAMESPACE, *PORT), // DNS: $(statefulset name)-$(ordinal).$(service name).$(namespace).svc.cluster.local
            connected: false });
    };
    topo
}