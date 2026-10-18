export default function CharacterCard({ character, isModerator, onViewBuilds, onEdit, onDelete }) {
  return (
    <div className={`card rarity-${character.rarity}`}>
      <div className="card-header">
        <h3>{character.name}</h3>
        <span className="rarity-badge">{'★'.repeat(character.rarity)}</span>
      </div>
      <p className="card-meta">
        <span className={`element-tag ${character.element.toLowerCase()}`}>{character.element}</span>
        <span className="weapon-tag">{character.weapon_type}</span>
      </p>
      <p className="card-region">📍 {character.region}</p>
      <p className="card-desc">{character.description}</p>
      <div className="card-actions">
        <button className="view-btn" onClick={() => onViewBuilds(character.id)}>
          View Builds
        </button>
        {isModerator && (
          <>
            <button className="edit-btn" onClick={() => onEdit(character)}>✏️</button>
            <button className="delete-btn" onClick={() => onDelete(character.id, character.name)}>🗑️</button>
          </>
        )}
      </div>
    </div>
  )
}