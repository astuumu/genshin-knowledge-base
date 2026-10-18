import CharacterCard from './CharacterCard'

export default function CharacterTab({
  characters,
  loading,
  searchQuery,
  setSearchQuery,
  selectedElement,
  setSelectedElement,
  selectedWeapon,
  setSelectedWeapon,
  elements,
  weaponTypes,
  isModerator,
  onOpenCreateModal,
  onViewBuilds,
  onEditCharacter,
  onDeleteCharacter
}) {
  const filtered = characters.filter((char) => {
    const matchesElem = selectedElement === 'All' || char.element === selectedElement
    const matchesWep = selectedWeapon === 'All' || char.weapon_type === selectedWeapon
    const matchesSearch = char.name.toLowerCase().includes(searchQuery.toLowerCase())
    return matchesElem && matchesWep && matchesSearch
  })

  return (
    <>
      <div className="filter-panel">
        <div className="filter-top-bar">
          <input
            type="text"
            placeholder="Search character name..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
          {isModerator && (
            <button className="add-char-btn" onClick={onOpenCreateModal}>
              + Add Character
            </button>
          )}
        </div>

        <div className="filter-group">
          <label>Element:</label>
          <div className="button-group">
            {elements.map((elem) => (
              <button
                key={elem}
                className={selectedElement === elem ? 'active' : ''}
                onClick={() => setSelectedElement(elem)}
              >
                {elem}
              </button>
            ))}
          </div>
        </div>

        <div className="filter-group">
          <label>Weapon:</label>
          <div className="button-group">
            {weaponTypes.map((wep) => (
              <button
                key={wep}
                className={selectedWeapon === wep ? 'active' : ''}
                onClick={() => setSelectedWeapon(wep)}
              >
                {wep}
              </button>
            ))}
          </div>
        </div>
      </div>

      {loading ? (
        <p className="status-text">Loading characters...</p>
      ) : (
        <div className="character-grid">
          {filtered.map((char) => (
            <CharacterCard
              key={char.id}
              character={char}
              isModerator={isModerator}
              onViewBuilds={onViewBuilds}
              onEdit={onEditCharacter}
              onDelete={onDeleteCharacter}
            />
          ))}
        </div>
      )}
    </>
  )
}