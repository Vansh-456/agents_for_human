import { useState } from 'react';

interface VendorInputProps {
  onSuccess: () => void;
}

export const VendorInput: React.FC<VendorInputProps> = ({ onSuccess }) => {
  const [message, setMessage] = useState('');
  const [mode, setMode] = useState<'natural' | 'structured'>('natural');

  // Structured fields
  const [quantity, setQuantity] = useState('');
  const [prepTime, setPrepTime] = useState('');
  const [deadline, setDeadline] = useState('');

  const submitNaturalLanguage = async () => {
    try {
      await fetch('http://localhost:8000/api/events/webhook/whatsapp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sender_id: 'vendor_1', text: message })
      });
      setMessage('');
      onSuccess();
    } catch (err) {
      console.error(err);
    }
  };

  const submitStructured = async () => {
    const text = `${quantity} meals ready, prepared ${prepTime} mins ago, pickup within ${deadline} mins.`;
    try {
      await fetch('http://localhost:8000/api/events/webhook/whatsapp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sender_id: 'vendor_1', text })
      });
      setQuantity('');
      setPrepTime('');
      setDeadline('');
      onSuccess();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="metric-card" style={{marginTop: '2rem'}}>
      <div className="section-title">Report Surplus</div>
      
      <div style={{display: 'flex', gap: '1rem', marginBottom: '1rem'}}>
        <button 
          className="btn" 
          style={{opacity: mode === 'natural' ? 1 : 0.5}}
          onClick={() => setMode('natural')}
        >
          Natural Language
        </button>
        <button 
          className="btn" 
          style={{opacity: mode === 'structured' ? 1 : 0.5}}
          onClick={() => setMode('structured')}
        >
          Structured
        </button>
      </div>

      {mode === 'natural' ? (
        <div>
          <textarea
            style={{width: '100%', height: '80px', marginBottom: '1rem', padding: '0.5rem', background: 'var(--bg)', color: 'var(--text)', border: '1px solid var(--border)'}}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="e.g. 45 vegetarian meals ready. Prepared 25 mins ago. Need pickup in 40 mins."
          />
          <button className="btn" onClick={submitNaturalLanguage} style={{background: 'var(--success)', border: 'none'}}>Send Message</button>
        </div>
      ) : (
        <div style={{display: 'flex', flexDirection: 'column', gap: '0.5rem'}}>
          <input 
            type="number" 
            placeholder="Quantity (meals)" 
            value={quantity} 
            onChange={(e) => setQuantity(e.target.value)}
            style={{padding: '0.5rem', background: 'var(--bg)', color: 'var(--text)', border: '1px solid var(--border)'}}
          />
          <input 
            type="number" 
            placeholder="Prepared mins ago" 
            value={prepTime} 
            onChange={(e) => setPrepTime(e.target.value)}
            style={{padding: '0.5rem', background: 'var(--bg)', color: 'var(--text)', border: '1px solid var(--border)'}}
          />
          <input 
            type="number" 
            placeholder="Pickup deadline (mins)" 
            value={deadline} 
            onChange={(e) => setDeadline(e.target.value)}
            style={{padding: '0.5rem', background: 'var(--bg)', color: 'var(--text)', border: '1px solid var(--border)'}}
          />
          <button className="btn" onClick={submitStructured} style={{background: 'var(--success)', border: 'none'}}>Submit Simulation</button>
        </div>
      )}
    </div>
  );
};
