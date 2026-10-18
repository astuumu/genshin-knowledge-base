export default function TeamCard({ team, isModerator, onEdit, onDelete }) {
  return (
    <div className="team-card">
      <div className="team-header">
        <div>
          <h2>{team.name}</h2>
          <span className={`team-badge ${team.team_type.toLowerCase()}`}>{team.team_type}</span>
        </div>
        {isModerator && (
          <div className="team-mod-actions">
            <button className="edit-btn-sm" onClick={() => onEdit(team)}>✏️ Edit</button>
            <button className="delete-btn-sm" onClick={() => onDelete(team.id, team.name)}>🗑️ Delete</button>
          </div>
        )}
      </div>
      <p className="team-desc">{team.description}</p>

      <div className="team-members-grid">
        {team.members?.map((member) => (
          <div key={member.id} className="member-slot">
            <div className="member-top">
              <span className={`element-tag ${member.character?.element?.toLowerCase()}`}>
                {member.character?.element}
              </span>
              <span className="member-rarity">{'★'.repeat(member.character?.rarity || 5)}</span>
            </div>
            <h4 className="member-name">{member.character?.name}</h4>
            <span className="member-role">{member.role}</span>
            {member.notes && <p className="member-notes">{member.notes}</p>}
          </div>
        ))}
      </div>
    </div>
  )
}