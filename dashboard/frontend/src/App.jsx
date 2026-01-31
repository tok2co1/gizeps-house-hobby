import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Play, Square, Activity, Image as ImageIcon, Terminal, Zap, Package, RefreshCw, PenTool } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import './App.css';

const API_BASE = 'http://localhost:8000';

function App() {
  const [status, setStatus] = useState({
    is_running: false,
    generated_today: 0,
    daily_limit: 25,
    last_image: null,
    current_task: "Beklemede",
    logs: [],
    custom_prompt: ""
  });
  const [customPrompt, setCustomPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const logContainerRef = useRef(null);
  const [userIsScrolling, setUserIsScrolling] = useState(false);

  const fetchStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE}/status`);
      setStatus(prev => {
        // Sadece loglar gerçekten değiştiyse state'i güncelle (gereksiz render engelleme)
        if (JSON.stringify(prev.logs) === JSON.stringify(response.data.logs)) {
          return { ...response.data, logs: prev.logs };
        }
        return response.data;
      });
    } catch (error) {
      console.error("API Hatası:", error);
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 3000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const container = logContainerRef.current;
    if (container) {
      // Eğer kullanıcı en aşağıya yakınsa otomatik kaydır
      const isAtBottom = container.scrollHeight - container.scrollTop <= container.clientHeight + 100;
      if (isAtBottom) {
        container.scrollTo({
          top: container.scrollHeight,
          behavior: 'smooth'
        });
      }
    }
  }, [status.logs]);

  const handleStart = async () => {
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/start`, {
        custom_prompt: customPrompt || null
      });
      fetchStatus();
    } catch (error) {
      console.error("Başlatma hatası:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleStop = async () => {
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/stop`);
      fetchStatus();
    } catch (error) {
      console.error("Durdurma hatası:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard-container">
      <header>
        <div className="flicker">
          <h1>Rubon Fabrikası <span style={{ color: 'var(--neon-pink)' }}>v3.0</span></h1>
          <p style={{ color: '#888', letterSpacing: '2px' }}>OTONOM ÜRETİM BİRİMİ</p>
        </div>
        <div className={`status-badge ${status.is_running ? 'status-running' : 'status-stopped'}`}>
          {status.is_running ? '● SİSTEM AKTİF' : '○ SİSTEM BEKLEMEDE'}
        </div>
      </header>

      <div className="grid-layout">
        <main>
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-label">Günlük Üretim</div>
              <div className="stat-value">{status.generated_today} / {status.daily_limit}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Mevcut Görev</div>
              <div className="stat-value" style={{ color: 'var(--neon-blue)' }}>{status.current_task}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Sistem Yükü</div>
              <div className="stat-value">STABİL</div>
            </div>
          </div>

          <div className="panel" style={{ marginBottom: '30px' }}>
            <h2><PenTool size={20} /> Tasarım Tarzı / Özel İstek</h2>
            <textarea
              className="custom-prompt-input"
              placeholder="Ne tarz bir çalışma istersiniz? (Örn: Vintage kahve dükkanı, Cyberpunk kurt logoları... Boş bırakılırsa rastgele üretir)"
              value={customPrompt}
              onChange={(e) => setCustomPrompt(e.target.value)}
              disabled={status.is_running}
            />
            <div className="controls">
              <button
                className="btn-start"
                onClick={handleStart}
                disabled={status.is_running || loading}
              >
                <Play size={20} fill="currentColor" /> Fabrikayı Başlat
              </button>
              <button
                className="btn-stop"
                onClick={handleStop}
                disabled={!status.is_running || loading}
              >
                <Square size={20} fill="currentColor" /> Acil Durdurma
              </button>
            </div>
          </div>

          <div className="panel">
            <h2><Terminal size={20} /> Sinir Ağı Kayıtları (Loglar)</h2>
            <div className="log-container" ref={logContainerRef}>
              {status.logs.map((log, i) => (
                <div key={i} className="log-entry">{log}</div>
              ))}
            </div>
          </div>
        </main>

        <aside>
          <div className="panel" style={{ height: '100%' }}>
            <h2><ImageIcon size={20} /> Üretim Çıktısı</h2>
            {status.last_image ? (
              <motion.div
                className="image-card"
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                key={status.last_image}
              >
                <img src={`${API_BASE}/output/${status.last_image}`} alt="Son Üretim" />
                <div className="image-label">SON_BİRİM: {status.last_image}</div>
              </motion.div>
            ) : (
              <div className="image-card" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#444' }}>
                <RefreshCw size={48} className="flicker" />
              </div>
            )}

            <div style={{ marginTop: '20px', fontSize: '0.8rem', color: '#666' }}>
              <p>📍 Konum: C:\...\rubon-factory\output</p>
              <p style={{ marginTop: '10px' }}><Package size={14} style={{ verticalAlign: 'middle' }} /> Arşivleme aktif</p>
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}

export default App;
