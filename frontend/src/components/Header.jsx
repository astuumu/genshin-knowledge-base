export default function Header({ 
  activeTab, 
  setActiveTab, 
  currentUser, 
  onLogout, 
  onOpenAbout, 
  reviewsCount 
}) {
  return (
    <header className="header">
      <div className="top-header-row">
        <button className="info-badge-btn" onClick={onOpenAbout}>
          ℹ️ About & Roles
        </button>

        <div className="auth-bar">
          {!currentUser ? (
            <div id="google-btn"></div>
          ) : (
            <div className="user-badge">
              <span>👤 {currentUser.username} ({currentUser.role})</span>
              <button onClick={onLogout} className="logout-btn">Log Out</button>
            </div>
          )}
        </div>
      </div>

      <h1>Genshin Impact Knowledge Base</h1>
      <p>Interactive character builds, weapon guides, meta teams, and community reviews</p>

      <nav className="tab-nav">
        <button 
          className={`tab-btn ${activeTab === 'characters' ? 'active' : ''}`}
          onClick={() => setActiveTab('characters')}
        >
          🗡️ Characters & Builds
        </button>
        <button 
          className={`tab-btn ${activeTab === 'teams' ? 'active' : ''}`}
          onClick={() => setActiveTab('teams')}
        >
          👥 Team Compositions
        </button>
        <button 
          className={`tab-btn ${activeTab === 'reviews' ? 'active' : ''}`}
          onClick={() => setActiveTab('reviews')}
        >
          ⭐ Community Reviews ({reviewsCount})
        </button>
      </nav>
    </header>
  )
}