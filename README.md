# Proxmox HA Cluster & Hybrid-Cloud Pipeline

## Project Overview

### Objective

The primary objective of this project is to engineer a resilient, production-grade High-Performance Computing (HPC) research environment. By utilizing a 3-node Proxmox HA Cluster, the architecture aims to eliminate single points of failure while implementing a Zero-Trust security model for off-site data archival. The project demonstrates the integration of Infrastructure as Code (IaC) and Full-Stack Observability to minimize the Mean Time to Recovery (MTTR) and ensure 24/7 availability for compute-intensive workloads.

### Project Phases

#### Phase 1: High-Availability Foundation

Establishing the physical and logical cluster. This phase focuses on the "Ground Truth" of the data center:

* Cluster Engineering: Deployment of three Proxmox VE nodes with dedicated Corosync networking to prevent split-brain scenarios.
* Storage Fabric: Configuration of hyper-converged shared storage (Ceph/NFS) to facilitate live migration and automated VM failover.

#### Phase 2: Declarative Configuration (IaC)

Transitioning from manual administration to automated lifecycle management:

* Ansible Orchestration: Development of playbooks to standardize environment variables, security patches, and SSH hardening across all nodes.
* Configuration Drift Control: Ensuring that any manual changes are automatically corrected by the centralized Ansible inventory.

#### Phase 3: Secure Hybrid-Cloud Data Pipeline

Extending the local data center to the cloud with a focus on data sovereignty:

* Encrypted Backups: Engineering a Python-based utility (boto3) that performs client-side AES-256 encryption using GPG before data egress.
* Cloud Archival: Automated synchronization of VM snapshots to AWS S3, utilizing IAM roles for least-privilege access.

#### Phase 4: Real-Time Observability & Alerting

Implementing a "Single Pane of Glass" for cluster health:

* Telemetry Stack: Deployment of Prometheus for time-series data collection and Grafana for visual analytics.
* Proactive Alerting: Authoring declarative rules in Alertmanager to achieve a Mean Time to Detect (MTTD) of under 60 seconds for hardware failures.

#### Phase 5: Disaster Recovery & Validation (The Fire Drill)

The final verification of the infrastructure's resilience:

* Recovery Engineering: Automating the restoration process from AWS S3, involving remote fetch, decryption, and hypervisor re-provisioning.
* RTO Benchmarking: Validating the Recovery Time Objective (RTO) against research-standard SLAs (15-minute restoration target).

### Implementation

#### Phase: 01 Building the foundation

* Multi-Node Hypervisor Orchestration Successfully deployed and synchronized three physical Proxmox VE 8.x nodes (pve-01, pve-02, pve-03) into a unified management cluster. This setup provides a single-pane-of-glass view of the entire compute pool and enables centralized resource scheduling.

* Dedicated Corosync Fabric for Quorum Configured a dedicated, low-latency network interface for Corosync communication. By isolating cluster heartbeat traffic from standard VM data traffic, I ensured Quorum stability and prevented "Split-Brain" scenarios, where nodes might attempt to start the same VM simultaneously.

* Converged Storage & HA Replication Implemented a shared storage fabric (ZFS Replication/NFS) to ensure VM disk images are consistent across all nodes. This architecture is the prerequisite for High Availability (HA), allowing the cluster to detect a node failure and automatically "resurrect" affected VMs on a healthy host.

* Proactive Fencing & Failover Policies Defined strict HA "Fencing" policies to manage how the cluster reacts during a hardware outage. I configured specialized HA Groups to prioritize critical workloads (like our HPC worker nodes), ensuring they are the first to be recovered during a re-fencing event.

* Live Migration (Zero-Downtime Maintenance) Validated the networking and storage stack by performing Live Migrations. This allows for the movement of running virtual machines between physical hosts with zero packet loss or downtime, a critical requirement for performing host hardware maintenance without interrupting research computations.

<table>
  <tr>
    Summary of a Node
  </tr>
  <tr>
    <td>
      <p>ISO</p>
    </td>
    <td>
      <p>Proxmox 9.1</p>
    </td>
  </tr>
  <tr>
    <td>
      <p>OS</p>
    </td>
    <td>
      <p>Debian 12/13</p>
    </td>
  </tr>
    <tr>
    <td>
      <p>Memory</p>
    </td>
    <td>
      <p>12288 MiB</p>
    </td>
  </tr>
  </tr>
    <tr>
    <td>
      <p>CPU</p>
    </td>
    <td>
      <p>4 Cores (Host-Passthrough)</p>
    </td>
  </tr>
  <tr>
    <td>
      <p>Storage</p>
    </td>
    <td>
      <p>100 GiB</p>
    </td>
  </tr>
</table>

#### Phase: 02 Declarative Configuration (IaC)