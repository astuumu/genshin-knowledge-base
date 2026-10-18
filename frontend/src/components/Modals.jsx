export default function Modals({
  showAbout,
  onCloseAbout,
  isCreatingChar,
  onCloseCreateChar,
  newCharData,
  setNewCharData,
  onCreateChar,
  editingChar,
  onCloseEditChar,
  editRegion,
  setEditRegion,
  editDesc,
  setEditDesc,
  onSaveEditChar,
  selectedCharDetails,
  onCloseCharDetails,
  loadingDetails,
  isModerator,
  isCreatingBuild,
  setIsCreatingBuild,
  editingBuild,
  setEditingBuild,
  buildForm,
  setBuildForm,
  onSaveBuild,
  onDeleteBuild,
  teamModalOpen,
  onCloseTeamModal,
  editingTeamId,
  teamForm,
  setTeamForm,
  onSaveTeam,
  characters,
  elements,
  weaponTypes,
  teamRoles,
  teamTypes
}) {
  return (
    <>
      {showAbout && (
        <div className="modal-backdrop" onClick={onCloseAbout}>
          <div className="modal-content about-modal" onClick={(e) => e.stopPropagation()}>
            <button className="close-btn" onClick={onCloseAbout}>×</button>
            <h2>ℹ️ About Genshin Knowledge Base</h2>
            <div className="about-section">
              <h3>📌 Project Overview & Purpose</h3>
              <p>
                Interactive knowledge base providing character builds, weapon guide rankings,
                and synergistic team compositions for Genshin Impact.
              </p>
              <h3>🛡️ Roles & Permissions</h3>
              <div className="roles-grid">
                <div className="role-card">
                  <h4>👤 Standard User</h4>
                  <ul>
                    <li>Browse guides and apply search filters.</li>
                    <li>Submit reviews and link them to entities.</li>
                    <li>Participate in community discussions.</li>
                  </ul>
                </div>
                <div className="role-card mod-card">
                  <h4>🛡️ Moderator</h4>
                  <ul>
                    <li>Manage characters and builds (CRUD).</li>
                    <li>Compose and publish meta teams.</li>
                    <li>Moderate community discussions.</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {isCreatingChar && (
        <div className="modal-backdrop" onClick={onCloseCreateChar}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="close-btn" onClick={onCloseCreateChar}>×</button>
            <h2>Add New Character</h2>
            <div className="edit-form">
              <label>Name:</label>
              <input 
                type="text" 
                value={newCharData.name} 
                onChange={(e) => setNewCharData({...newCharData, name: e.target.value})} 
                className="search-input" 
              />
              <div className="form-row">
                <div>
                  <label>Element:</label>
                  <select 
                    value={newCharData.element} 
                    onChange={(e) => setNewCharData({...newCharData, element: e.target.value})} 
                    className="search-input"
                  >
                    {elements.filter(e => e !== 'All').map(e => <option key={e} value={e}>{e}</option>)}
                  </select>
                </div>
                <div>
                  <label>Weapon:</label>
                  <select 
                    value={newCharData.weapon_type} 
                    onChange={(e) => setNewCharData({...newCharData, weapon_type: e.target.value})} 
                    className="search-input"
                  >
                    {weaponTypes.filter(w => w !== 'All').map(w => <option key={w} value={w}>{w}</option>)}
                  </select>
                </div>
                <div>
                  <label>Rarity:</label>
                  <select 
                    value={newCharData.rarity} 
                    onChange={(e) => setNewCharData({...newCharData, rarity: Number(e.target.value)})} 
                    className="search-input"
                  >
                    <option value={5}>5 ★</option>
                    <option value={4}>4 ★</option>
                  </select>
                </div>
              </div>
              <label>Region:</label>
              <input 
                type="text" 
                value={newCharData.region} 
                onChange={(e) => setNewCharData({...newCharData, region: e.target.value})} 
                className="search-input" 
              />
              <label>Description:</label>
              <textarea 
                rows={3} 
                value={newCharData.description} 
                onChange={(e) => setNewCharData({...newCharData, description: e.target.value})} 
                className="search-input" 
              />
              <button className="save-btn" onClick={onCreateChar}>Create Character</button>
            </div>
          </div>
        </div>
      )}

      {editingChar && (
        <div className="modal-backdrop" onClick={onCloseEditChar}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="close-btn" onClick={onCloseEditChar}>×</button>
            <h2>Edit {editingChar.name}</h2>
            <div className="edit-form">
              <label>Region:</label>
              <input 
                type="text" 
                value={editRegion} 
                onChange={(e) => setEditRegion(e.target.value)} 
                className="search-input" 
              />
              <label>Description:</label>
              <textarea 
                value={editDesc} 
                onChange={(e) => setEditDesc(e.target.value)} 
                rows={4} 
                className="search-input" 
              />
              <button className="save-btn" onClick={onSaveEditChar}>Save Changes</button>
            </div>
          </div>
        </div>
      )}

      {teamModalOpen && (
        <div className="modal-backdrop" onClick={onCloseTeamModal}>
          <div className="modal-content team-modal" onClick={(e) => e.stopPropagation()}>
            <button className="close-btn" onClick={onCloseTeamModal}>×</button>
            <h2>{editingTeamId ? 'Edit Team Composition' : 'Create New Team Composition'}</h2>
            <div className="edit-form">
              <label>Team Name:</label>
              <input 
                type="text" 
                value={teamForm.name} 
                onChange={(e) => setTeamForm({...teamForm, name: e.target.value})} 
                className="search-input" 
              />
              <label>Team Type:</label>
              <select 
                value={teamForm.team_type} 
                onChange={(e) => setTeamForm({...teamForm, team_type: e.target.value})} 
                className="search-input"
              >
                {teamTypes.map(t => <option key={t} value={t}>{t}</option>)}
              </select>
              <label>Strategy & Playstyle:</label>
              <textarea 
                rows={2} 
                value={teamForm.description} 
                onChange={(e) => setTeamForm({...teamForm, description: e.target.value})} 
                className="search-input" 
              />
              <h3>Team Members (4 Characters)</h3>
              <div className="team-builder-slots">
                {teamForm.members.map((member, idx) => (
                  <div key={idx} className="builder-slot">
                    <span className="slot-title">Slot {idx + 1}</span>
                    <label>Character:</label>
                    <select 
                      value={member.character_id} 
                      onChange={(e) => {
                        const updated = [...teamForm.members]
                        updated[idx].character_id = e.target.value
                        setTeamForm({ ...teamForm, members: updated })
                      }} 
                      className="search-input"
                    >
                      <option value="">-- Choose --</option>
                      {characters.map(c => <option key={c.id} value={c.id}>{c.name} ({c.element})</option>)}
                    </select>
                    <label>Role:</label>
                    <select 
                      value={member.role} 
                      onChange={(e) => {
                        const updated = [...teamForm.members]
                        updated[idx].role = e.target.value
                        setTeamForm({ ...teamForm, members: updated })
                      }} 
                      className="search-input"
                    >
                      {teamRoles.map(r => <option key={r} value={r}>{r}</option>)}
                    </select>
                    <label>Role Notes:</label>
                    <input 
                      type="text" 
                      value={member.notes} 
                      onChange={(e) => {
                        const updated = [...teamForm.members]
                        updated[idx].notes = e.target.value
                        setTeamForm({ ...teamForm, members: updated })
                      }} 
                      className="search-input" 
                    />
                  </div>
                ))}
              </div>
              <div className="form-actions">
                <button className="save-btn" onClick={onSaveTeam}>Save Team</button>
                <button className="cancel-btn" onClick={onCloseTeamModal}>Cancel</button>
              </div>
            </div>
          </div>
        </div>
      )}

      {selectedCharDetails && (
        <div className="modal-backdrop" onClick={onCloseCharDetails}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="close-btn" onClick={onCloseCharDetails}>×</button>
            <h2>{selectedCharDetails.name} — Recommended Builds</h2>
            <p className="modal-subheading">
              {selectedCharDetails.element} | {selectedCharDetails.weapon_type} | {selectedCharDetails.region}
            </p>

            {isModerator && !isCreatingBuild && !editingBuild && (
              <button 
                className="add-build-btn" 
                onClick={() => {
                  setBuildForm({ role_title: '', stats_priority: '', notes: '' })
                  setIsCreatingBuild(true)
                }}
              >
                + Add New Build
              </button>
            )}

            {(isCreatingBuild || editingBuild) && (
              <div className="build-editor-box">
                <h3>{editingBuild ? 'Edit Build' : 'Create New Build'}</h3>
                <div className="edit-form">
                  <label>Role / Title:</label>
                  <input 
                    type="text" 
                    value={buildForm.role_title} 
                    onChange={(e) => setBuildForm({...buildForm, role_title: e.target.value})} 
                    className="search-input" 
                  />
                  <label>Artifact Stat Priority:</label>
                  <input 
                    type="text" 
                    value={buildForm.stats_priority} 
                    onChange={(e) => setBuildForm({...buildForm, stats_priority: e.target.value})} 
                    className="search-input" 
                  />
                  <label>Notes & Playstyle:</label>
                  <textarea 
                    rows={2} 
                    value={buildForm.notes} 
                    onChange={(e) => setBuildForm({...buildForm, notes: e.target.value})} 
                    className="search-input" 
                  />
                  <div className="form-actions">
                    <button className="save-btn" onClick={onSaveBuild}>Save Build</button>
                    <button className="cancel-btn" onClick={() => { setIsCreatingBuild(false); setEditingBuild(null); }}>Cancel</button>
                  </div>
                </div>
              </div>
            )}

            {loadingDetails ? (
              <p>Loading build details...</p>
            ) : (
              <div className="builds-section">
                {selectedCharDetails.builds?.map((build) => (
                  <div key={build.id} className="build-block">
                    <div className="build-header">
                      <h3>{build.role_title}</h3>
                      {isModerator && (
                        <div className="build-actions">
                          <button 
                            className="edit-btn-sm" 
                            onClick={() => {
                              setEditingBuild(build)
                              setBuildForm({
                                role_title: build.role_title,
                                stats_priority: build.stats_priority,
                                notes: build.notes || ''
                              })
                            }}
                          >
                            ✏️ Edit
                          </button>
                          <button className="delete-btn-sm" onClick={() => onDeleteBuild(build.id)}>🗑️ Delete</button>
                        </div>
                      )}
                    </div>
                    <p><strong>Artifact Stat Priority:</strong> {build.stats_priority}</p>
                    <p><em>{build.notes}</em></p>
                    <div className="build-columns">
                      <div className="gear-col">
                        <h4>Recommended Weapons</h4>
                        <ul>
                          {build.weapons?.map((w) => (
                            <li key={w.id}><strong>{w.weapon.name}</strong> ({w.weapon.rarity}★) — {w.priority}</li>
                          ))}
                        </ul>
                      </div>
                      <div className="gear-col">
                        <h4>Recommended Artifact Sets</h4>
                        <ul>
                          {build.artifact_sets?.map((a) => (
                            <li key={a.id}><strong>{a.artifact_set.name}</strong> ({a.set_type})</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </>
  )
}