import TeamCard from './TeamCard'

export default function TeamTab({
  teams,
  loading,
  isModerator,
  onOpenCreateTeam,
  onEditTeam,
  onDeleteTeam
}) {
  return (
    <div className="teams-view">
      {isModerator && (
        <div className="teams-action-bar">
          <button className="add-char-btn" onClick={onOpenCreateTeam}>
            + Create New Team
          </button>
        </div>
      )}

      {loading ? (
        <p className="status-text">Loading meta teams...</p>
      ) : (
        <div className="teams-grid">
          {teams.map((team) => (
            <TeamCard
              key={team.id}
              team={team}
              isModerator={isModerator}
              onEdit={onEditTeam}
              onDelete={onDeleteTeam}
            />
          ))}
        </div>
      )}
    </div>
  )
}