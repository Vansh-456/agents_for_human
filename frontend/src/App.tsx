import { useEffect, useState } from 'react';
import { VendorInput } from './components/VendorInput';
import './index.css';

const API_BASE = 'http://localhost:8000/api';

interface TimelineEvent {
  timestamp: string;
  agent: string;
  message: string;
}

interface NetworkState {
  vendors: any;
  ngos: any;
  riders: any;
  timeline: TimelineEvent[];
}

function App() {
  const [network, setNetwork] = useState<NetworkState | null>(null);

  const fetchNetwork = async () => {
    try {
      const res = await fetch(`${API_BASE}/network`);
      const data = await res.json();
      setNetwork(data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchNetwork();
    const interval = setInterval(fetchNetwork, 2000);
    return () => clearInterval(interval);
  }, []);

  const triggerSimulation = async (type: string) => {
    try {
      await fetch(`${API_BASE}/simulation/trigger/${type}`, { method: 'POST' });
      fetchNetwork();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="app-container">
      {/* Left Sidebar - Controls & Metrics */}
      <div className="glass-panel" style={{overflowY: 'auto'}}>
        <h1>AnnaSetu</h1>
        <div className="subtitle">Autonomous Food Rescue Mesh</div>

        <div className="section-title">Global State</div>
        <div className="metric-card">
          <div className="section-title" style={{marginBottom: 0}}>Meals Rescued Today</div>
          <div className="metric-value" style={{color: 'var(--success)'}}>327</div>
        </div>
        <div className="metric-card">
          <div className="section-title" style={{marginBottom: 0}}>At Risk (Approaching Expiry)</div>
          <div className="metric-value" style={{color: 'var(--warning)'}}>45</div>
        </div>

        <div className="section-title" style={{marginTop: '2rem'}}>Simulation Controls</div>
        <button className="btn" onClick={() => triggerSimulation('normal')}>
          🚀 Start: Normal Rescue
        </button>
        <button className="btn btn-warning" onClick={() => triggerSimulation('rider_failure')}>
          ⚠️ Start: Rider Cancellation
        </button>
        <button className="btn btn-danger" onClick={() => triggerSimulation('safety_block')}>
          🛑 Start: Safety Conflict
        </button>
      </div>

      {/* Main View - Network Status */}
      <div className="glass-panel" style={{overflowY: 'hidden'}}>
        <VendorInput onSuccess={fetchNetwork} />
        
        <div className="section-title" style={{marginTop: '2rem'}}>Live Network Map</div>
        <div className="network-view">
          <div>
            <h3 style={{marginBottom: '1rem', fontSize: '1rem'}}>Vendors (Surplus)</h3>
            <div className="network-grid">
              {network?.vendors && Object.entries(network.vendors).map(([id, v]: any) => (
                <div key={id} className="node-card">
                  <div className="node-icon" style={{background: 'rgba(59, 130, 246, 0.2)', color: '#3b82f6'}}>🏪</div>
                  <div className="node-info">
                    <span className="node-name">{v.name}</span>
                    <span className="node-stat">Trust: {v.trust_score * 100}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          <div>
            <h3 style={{marginBottom: '1rem', fontSize: '1rem'}}>NGOs (Capacity)</h3>
            <div className="network-grid">
              {network?.ngos && Object.entries(network.ngos).map(([id, n]: any) => (
                <div key={id} className="node-card">
                  <div className="node-icon" style={{background: 'rgba(16, 185, 129, 0.2)', color: '#10b981'}}>❤️</div>
                  <div className="node-info">
                    <span className="node-name">{n.name}</span>
                    <span className="node-stat">Slots: {n.current_capacity}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div>
            <h3 style={{marginBottom: '1rem', fontSize: '1rem'}}>Riders (Logistics)</h3>
            <div className="network-grid">
              {network?.riders && Object.entries(network.riders).map(([id, r]: any) => (
                <div key={id} className="node-card" style={{opacity: r.available ? 1 : 0.5}}>
                  <div className="node-icon" style={{background: 'rgba(245, 158, 11, 0.2)', color: '#f59e0b'}}>🛵</div>
                  <div className="node-info">
                    <span className="node-name">{r.name}</span>
                    <span className="node-stat">{r.available ? 'Available' : 'Busy'}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Right Sidebar - Agent Activity */}
      <div className="glass-panel">
        <div className="section-title">Live Agent Activity</div>
        <div className="timeline">
          {network?.timeline?.length === 0 && (
            <div style={{color: 'var(--text-muted)', textAlign: 'center', marginTop: '2rem'}}>
              Waiting for events...
            </div>
          )}
          {network?.timeline?.map((event, i) => (
            <div className="timeline-item" key={i}>
              <div className="timeline-time">{event.timestamp}</div>
              <div className="timeline-content" data-agent={event.agent}>
                <div className="timeline-agent">{event.agent}</div>
                <div className="timeline-message">{event.message}</div>
              </div>
            </div>
          )).reverse()}
        </div>
      </div>
    </div>
  );
}

export default App;
