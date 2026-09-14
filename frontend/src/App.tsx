import { useCallback, useEffect, useState } from 'react';
import type { FormEvent } from 'react';
import './index.css';

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000/api';
type RecordMap = Record<string, Record<string, any>>;

// Deeply typed NetworkState matching backend contracts
interface Plan {
  id: string;
  workflow_id: string;
  surplus_id: string;
  ngo_id: string;
  rider_id: string;
  quantity: number;
  eta_mins: number;
  safety_status: string;
  status: string;
  safety?: { safety_margin_mins?: number; reasons?: string[] };
}

interface Network { 
  vendors: RecordMap; 
  ngos: RecordMap; 
  riders: RecordMap; 
  surplus: any[]; 
  plans: Record<string, Plan>; 
  timeline: any[] 
}

const label = (value: string) => value.replaceAll('_', ' ').replace(/\b\w/g, (letter) => letter.toUpperCase());

export default function App() {
  const [network, setNetwork] = useState<Network | null>(null);
  const [message, setMessage] = useState('45 vegetarian meals ready, pickup within 42 minutes');
  const [notice, setNotice] = useState('Connecting to the rescue network…');
  const [loading, setLoading] = useState(false);

  const refresh = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE}/network/`);
      if (!response.ok) throw new Error('Network unavailable');
      setNetwork(await response.json());
      setNotice('Live operational data · updates every 3 seconds');
    } catch { setNotice('Demo API is unavailable. Start the backend on port 8000.'); }
  }, []);

  useEffect(() => { 
    refresh(); 
    const timer = window.setInterval(refresh, 3000); 
    return () => window.clearInterval(timer); 
  }, [refresh]);

  const runScenario = async (scenario: string) => {
    setLoading(true); setNotice(`Running ${label(scenario)} through the live workflow…`);
    try { 
      const response = await fetch(`${API_BASE}/simulation/trigger/${scenario}`, { method: 'POST' }); 
      if (!response.ok) throw new Error(); 
      await refresh(); 
      setNotice(`${label(scenario)} completed. Inspect the decision ledger below.`); 
    }
    catch { setNotice('Scenario could not run. Check the API and retry.'); }
    finally { setLoading(false); }
  };

  const submit = async (event: FormEvent) => {
    event.preventDefault(); if (!message.trim()) return;
    setLoading(true); setNotice('AnnaSetu is validating your report…');
    try { 
      const response = await fetch(`${API_BASE}/events/webhook/whatsapp`, { 
        method: 'POST', 
        headers: { 'Content-Type': 'application/json' }, 
        body: JSON.stringify({ sender_id: 'vendor_1', text: message }) 
      }); 
      if (!response.ok) throw new Error(); 
      await refresh(); 
      setNotice('Report processed. The decision trail is now visible.'); 
    }
    catch { setNotice('Unable to submit. Please retry after checking the API.'); }
    finally { setLoading(false); }
  };

  // Convert plans object to array for easier filtering
  const plans = network?.plans ? Object.values(network.plans) : []; 
  const delivered = plans.filter((plan) => plan.status === 'DELIVERED').reduce((sum, plan) => sum + plan.quantity, 0);
  const active = plans.filter((plan) => ['PROPOSED', 'SAFETY_PASS', 'RESERVED', 'ASSIGNED', 'ACCEPTED', 'PICKED_UP', 'IN_TRANSIT'].includes(plan.status));
  const reviewPlans = plans.filter((plan) => ['HUMAN_REVIEW', 'SAFETY_BLOCKED'].includes(plan.status));
  
  const handleOperatorAction = async (planId: string, action: string) => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/plans/${planId}/status`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: action })
      });
      if (!response.ok) throw new Error();
      await refresh();
    } catch {
      setNotice('Failed to submit operator decision.');
    } finally {
      setLoading(false);
    }
  };

  return <main>
    <header className="topbar">
      <div>
        <p className="eyebrow">AUTONOMOUS FOOD-RESCUE NETWORK</p>
        <h1>Anna<span>Setu</span></h1>
      </div>
      <div className="live"><i /> {notice}</div>
    </header>

    <section className="hero">
      <div>
        <p className="eyebrow">GOOD NEIGHBOR AGENT · DELHI NCR PILOT</p>
        <h2>Turn surplus into <em>safe, delivered meals.</em></h2>
        <p>AnnaSetu coordinates donors, community kitchens and riders in the background—then only asks people when a genuine decision needs them.</p>
      </div>
      <div className="guard">
        <span>ANNA<span>GUARD</span></span>
        <strong>{active[0]?.safety_status ?? (reviewPlans[0]?.safety_status ?? 'READY')}</strong>
        <small>Deterministic safety control plane</small>
      </div>
    </section>

    <section className="metrics">
      <Metric value={String(delivered)} label="Meals delivered" tone="green"/>
      <Metric value={String(active.length)} label="Active rescues" tone="blue"/>
      <Metric value={String((network?.riders && Object.values(network.riders).filter((r: any) => r.available).length) ?? 0)} label="Riders ready"/>
      <Metric value={String(plans.filter((p) => p.status === 'FAILED').length)} label="Auto-recoveries" tone="amber"/>
    </section>

    {reviewPlans.length > 0 && (
      <section className="panel" style={{ marginBottom: 24, border: '1px solid var(--accent-warning)', background: 'rgba(245,158,11,0.05)' }}>
        <div className="panel-head">
          <div><p className="eyebrow" style={{ color: 'var(--accent-warning)' }}>HUMAN INBOX</p><h3>Review Required</h3></div>
          <span className="tag" style={{ color: 'var(--accent-warning)', borderColor: 'var(--accent-warning)' }}>ACTION NEEDED</span>
        </div>
        <div style={{ marginTop: 16 }}>
          {reviewPlans.map(plan => (
            <div key={plan.id} style={{ padding: 16, background: 'rgba(0,0,0,0.3)', borderRadius: 12, marginBottom: 12, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <b style={{ display: 'block', marginBottom: 4 }}>Plan {plan.id} - {plan.status}</b>
                <span style={{ fontSize: 13, color: 'var(--text-secondary)' }}>
                  {plan.quantity} meals • ETA {plan.eta_mins} mins • {plan.safety?.reasons?.join(', ') || 'Manual review triggered'}
                </span>
              </div>
              <div style={{ display: 'flex', gap: 8 }}>
                <button disabled={loading} onClick={() => handleOperatorAction(plan.id, 'CANCELLED')} style={{ padding: '8px 16px', background: 'var(--bg-panel)', border: '1px solid var(--border-color)', color: 'var(--text-primary)', margin: 0, width: 'auto' }}>Reject</button>
                <button disabled={loading} onClick={() => handleOperatorAction(plan.id, 'ASSIGNED')} style={{ padding: '8px 16px', background: 'var(--accent-warning)', color: '#000', margin: 0, width: 'auto' }}>Force Approve</button>
              </div>
            </div>
          ))}
        </div>
      </section>
    )}

    <section className="grid">
      <section className="panel report">
        <div className="panel-head">
          <div><p className="eyebrow">REPORT SURPLUS</p><h3>One message starts a rescue</h3></div>
          <span className="tag">STRANDS + BEDROCK</span>
        </div>
        <form onSubmit={submit}>
          <label htmlFor="message">Describe food, quantity, and pickup deadline</label>
          <textarea id="message" value={message} onChange={(e) => setMessage(e.target.value)} aria-label="Surplus report"/>
          <button disabled={loading}>{loading ? 'Processing…' : 'Start safe rescue'} <b>→</b></button>
        </form>
        <div className="scenarios">
          <p className="eyebrow">GUIDED DEMOS</p>
          {[['normal','Normal rescue'],['rider_failure','Rider failure → re-plan'],['safety_block','Safety block'],['clarification','Missing details']].map(([key, text]) => 
            <button key={key} className="scenario" disabled={loading} onClick={() => runScenario(key)}>
              {text}<span>↗</span>
            </button>
          )}
        </div>
      </section>

      <section className="panel route">
        <div className="panel-head">
          <div><p className="eyebrow">LIVE NETWORK</p><h3>Safe routes, visible decisions</h3></div>
          <span className="tag green">{active.length ? 'IN MOTION' : 'STANDING BY'}</span>
        </div>
        <div className="route-canvas">
          <div className="route-line"/>
          <Node icon="✦" title="Donor" text={network?.vendors?.vendor_1?.name ?? 'Restaurant A'} cls="donor"/>
          <Node icon="◉" title="Rider" text={active[0] ? network?.riders?.[active[0].rider_id]?.name ?? active[0].rider_id : 'Awaiting assignment'} cls="rider"/>
          <Node icon="♥" title="Recipient" text={active[0] ? network?.ngos?.[active[0].ngo_id]?.name ?? active[0].ngo_id : 'Capacity monitored'} cls="ngo"/>
        </div>
        {active[0] ? 
          <div className="plan-detail">
            <span><b>{active[0].quantity}</b> meals</span>
            <span><b>{active[0].eta_mins} min</b> ETA</span>
            <span><b>{active[0].safety?.safety_margin_mins ?? '—'} min</b> margin</span>
          </div> 
        : reviewPlans[0] ? 
          <p className="empty">Route is blocked pending human operator review.</p>
        : <p className="empty">Run a scenario to see an evidence-backed route.</p>}
      </section>

      <section className="panel ledger">
        <div className="panel-head">
          <div><p className="eyebrow">DECISION LEDGER</p><h3>Every action is explainable</h3></div>
          <span className="tag">AUDITABLE</span>
        </div>
        <div className="timeline">
          {(network?.timeline ?? []).slice().reverse().slice(0, 10).map((event, i) => 
            <article key={`${event.timestamp}-${i}`}>
              <time>{new Date(event.timestamp).toLocaleTimeString()}</time>
              <div>
                <b>{event.agent}</b>
                <p>{event.message}</p>
              </div>
            </article>
          )}
          {!network?.timeline?.length && <p className="empty">Events will appear here after a workflow starts.</p>}
        </div>
      </section>
    </section>

    <footer>Built with Strands Agents SDK · Amazon Bedrock · deterministic AnnaGuard policies · all operational metrics are derived from workflow records.</footer>
  </main>;
}

function Metric({ value, label, tone = '' }: { value: string; label: string; tone?: string }) { 
  return <article className={`metric ${tone}`}>
    <strong>{value}</strong>
    <span>{label}</span>
  </article>; 
}

function Node({ icon, title, text, cls }: { icon: string; title: string; text: string; cls: string }) { 
  return <div className={`map-node ${cls}`}>
    <i>{icon}</i>
    <div>
      <small>{title}</small>
      <b>{text}</b>
    </div>
  </div>; 
}
