import { useEffect, useState } from 'react'
import Header from './components/Header'
import CharacterTab from './components/CharacterTab'
import TeamTab from './components/TeamTab'
import ReviewTab from './components/ReviewTab'
import Modals from './components/Modals'
import './App.css'

const ELEMENTS = ['All', 'Pyro', 'Hydro', 'Cryo', 'Electro', 'Dendro', 'Anemo', 'Geo']
const WEAPON_TYPES = ['All', 'Sword', 'Claymore', 'Polearm', 'Bow', 'Catalyst']
const TEAM_ROLES = ['Main DPS', 'Sub DPS', 'Support', 'Healer', 'Shielder']
const TEAM_TYPES = ['Meta', 'F2P', 'Alternative', 'Fun']

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1'
const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID || ''

export default function App() {
  const [activeTab, setActiveTab] = useState('characters')

  const [characters, setCharacters] = useState([])
  const [loadingCharacters, setLoadingCharacters] = useState(true)
  const [selectedElement, setSelectedElement] = useState('All')
  const [selectedWeapon, setSelectedWeapon] = useState('All')
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCharDetails, setSelectedCharDetails] = useState(null)
  const [loadingDetails, setLoadingDetails] = useState(false)

  const [teams, setTeams] = useState([])
  const [loadingTeams, setLoadingTeams] = useState(true)

  const [reviews, setReviews] = useState([])
  const [loadingReviews, setLoadingReviews] = useState(false)
  const [newRating, setNewRating] = useState(5)
  const [newComment, setNewComment] = useState('')
  const [refType, setRefType] = useState('none')
  const [refId, setRefId] = useState('')
  const [replyTexts, setReplyTexts] = useState({})

  const [currentUser, setCurrentUser] = useState(() => {
    const saved = localStorage.getItem('user')
    return saved ? JSON.parse(saved) : null
  })
  const [authToken, setAuthToken] = useState(() => localStorage.getItem('token') || '')

  const [showAboutModal, setShowAboutModal] = useState(false)
  const [isCreatingChar, setIsCreatingChar] = useState(false)
  const [newCharData, setNewCharData] = useState({
    name: '', element: 'Pyro', weapon_type: 'Sword', rarity: 5, region: '', description: ''
  })
  const [editingChar, setEditingChar] = useState(null)
  const [editDesc, setEditDesc] = useState('')
  const [editRegion, setEditRegion] = useState('')

  const [editingBuild, setEditingBuild] = useState(null)
  const [isCreatingBuild, setIsCreatingBuild] = useState(false)
  const [buildForm, setBuildForm] = useState({ role_title: '', stats_priority: '', notes: '' })

  const [teamModalOpen, setTeamModalOpen] = useState(false)
  const [editingTeamId, setEditingTeamId] = useState(null)
  const [teamForm, setTeamForm] = useState({
    name: '', team_type: 'Meta', description: '',
    members: [
      { character_id: '', role: 'Main DPS', notes: '' },
      { character_id: '', role: 'Sub DPS', notes: '' },
      { character_id: '', role: 'Support', notes: '' },
      { character_id: '', role: 'Healer', notes: '' }
    ]
  })

  useEffect(() => {
    fetchCharacters()
    fetchTeams()
    fetchReviews()

    if (window.google && GOOGLE_CLIENT_ID) {
      window.google.accounts.id.initialize({
        client_id: GOOGLE_CLIENT_ID,
        callback: handleGoogleResponse
      })
      window.google.accounts.id.renderButton(
        document.getElementById('google-btn'),
        { theme: 'outline', size: 'medium' }
      )
    }
  }, [])

  const fetchCharacters = async () => {
    try {
      const res = await fetch(`${API_BASE}/characters`)
      const json = await res.json()
      setCharacters(json.data || [])
    } catch (err) {
      console.error(err)
    } finally {
      setLoadingCharacters(false)
    }
  }

  const fetchTeams = async () => {
    try {
      const res = await fetch(`${API_BASE}/teams`)
      const json = await res.json()
      setTeams(json.data || [])
    } catch (err) {
      console.error(err)
    } finally {
      setLoadingTeams(false)
    }
  }

  const fetchReviews = async () => {
    setLoadingReviews(true)
    try {
      const res = await fetch(`${API_BASE}/reviews`)
      const json = await res.json()
      setReviews(json.data || [])
    } catch (err) {
      console.error(err)
    } finally {
      setLoadingReviews(false)
    }
  }

  const handleGoogleResponse = async (response) => {
    try {
      const res = await fetch(`${API_BASE}/auth/google`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token: response.credential })
      })
      const data = await res.json()
      if (data.token) {
        setCurrentUser(data.user)
        setAuthToken(data.token)
        localStorage.setItem('token', data.token)
        localStorage.setItem('user', JSON.stringify(data.user))
      }
    } catch (err) {
      console.error('Auth failure:', err)
    }
  }

  const handleLogout = () => {
    setCurrentUser(null)
    setAuthToken('')
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  const fetchCharacterDetails = async (id) => {
    setLoadingDetails(true)
    try {
      const res = await fetch(`${API_BASE}/characters/${id}`)
      const data = await res.json()
      setSelectedCharDetails(data.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoadingDetails(false)
    }
  }

  const handleCreateCharacter = async () => {
    try {
      const res = await fetch(`${API_BASE}/characters`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${authToken}` },
        body: JSON.stringify(newCharData)
      })
      if (!res.ok) throw new Error('Failed to create character')
      setIsCreatingChar(false)
      setNewCharData({ name: '', element: 'Pyro', weapon_type: 'Sword', rarity: 5, region: '', description: '' })
      fetchCharacters()
    } catch (err) {
      alert(err.message)
    }
  }

  const handleDeleteCharacter = async (charId, charName) => {
    if (!window.confirm(`Delete "${charName}"?`)) return
    try {
      const res = await fetch(`${API_BASE}/characters/${charId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${authToken}` }
      })
      if (!res.ok) throw new Error('Deletion rejected')
      fetchCharacters()
      fetchTeams()
    } catch (err) {
      alert(err.message)
    }
  }

  const handleSaveCharacterEdit = async () => {
    try {
      const res = await fetch(`${API_BASE}/characters/${editingChar.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${authToken}` },
        body: JSON.stringify({ description: editDesc, region: editRegion })
      })
      if (!res.ok) throw new Error('Update failed')
      setEditingChar(null)
      fetchCharacters()
    } catch (err) {
      alert(err.message)
    }
  }

  const handleSaveBuild = async () => {
    const isEdit = Boolean(editingBuild)
    const url = isEdit ? `${API_BASE}/builds/${editingBuild.id}` : `${API_BASE}/characters/${selectedCharDetails.id}/builds`

    try {
      const res = await fetch(url, {
        method: isEdit ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${authToken}` },
        body: JSON.stringify(buildForm)
      })
      if (!res.ok) throw new Error('Build operation failed')
      setIsCreatingBuild(false)
      setEditingBuild(null)
      fetchCharacterDetails(selectedCharDetails.id)
    } catch (err) {
      alert(err.message)
    }
  }

  const handleDeleteBuild = async (buildId) => {
    if (!window.confirm('Delete this build?')) return
    try {
      const res = await fetch(`${API_BASE}/builds/${buildId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${authToken}` }
      })
      if (!res.ok) throw new Error('Delete build failed')
      fetchCharacterDetails(selectedCharDetails.id)
    } catch (err) {
      alert(err.message)
    }
  }

  const handleOpenCreateTeam = () => {
    setEditingTeamId(null)
    const defaultCharId = characters.length > 0 ? characters[0].id : ''
    setTeamForm({
      name: '', team_type: 'Meta', description: '',
      members: [
        { character_id: defaultCharId, role: 'Main DPS', notes: '' },
        { character_id: defaultCharId, role: 'Sub DPS', notes: '' },
        { character_id: defaultCharId, role: 'Support', notes: '' },
        { character_id: defaultCharId, role: 'Healer', notes: '' }
      ]
    })
    setTeamModalOpen(true)
  }

  const handleOpenEditTeam = (team) => {
    setEditingTeamId(team.id)
    setTeamForm({
      name: team.name,
      team_type: team.team_type,
      description: team.description || '',
      members: team.members.map(m => ({ character_id: m.character_id, role: m.role, notes: m.notes || '' }))
    })
    setTeamModalOpen(true)
  }

  const handleSaveTeam = async () => {
    const isEdit = Boolean(editingTeamId)
    const url = isEdit ? `${API_BASE}/teams/${editingTeamId}` : `${API_BASE}/teams`

    try {
      const res = await fetch(url, {
        method: isEdit ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${authToken}` },
        body: JSON.stringify({
          ...teamForm,
          members: teamForm.members.map(m => ({ ...m, character_id: Number(m.character_id) }))
        })
      })
      if (!res.ok) throw new Error('Save team failed')
      setTeamModalOpen(false)
      fetchTeams()
    } catch (err) {
      alert(err.message)
    }
  }

  const handleDeleteTeam = async (teamId, teamName) => {
    if (!window.confirm(`Delete team "${teamName}"?`)) return
    try {
      const res = await fetch(`${API_BASE}/teams/${teamId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${authToken}` }
      })
      if (!res.ok) throw new Error('Delete team failed')
      fetchTeams()
    } catch (err) {
      alert(err.message)
    }
  }

  const handleAddReview = async () => {
    if (!newComment.trim()) return

    let targetName = null
    if (refType === 'character') {
      const found = characters.find(c => String(c.id) === String(refId))
      targetName = found ? found.name : null
    } else if (refType === 'team') {
      const found = teams.find(t => String(t.id) === String(refId))
      targetName = found ? found.name : null
    }

    try {
      const res = await fetch(`${API_BASE}/reviews`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${authToken}` },
        body: JSON.stringify({
          rating: Number(newRating),
          comment: newComment,
          target_type: refType,
          target_id: refType !== 'none' && refId ? Number(refId) : null,
          target_name: targetName
        })
      })
      if (!res.ok) throw new Error('Posting review failed')
      setNewComment('')
      setRefType('none')
      setRefId('')
      fetchReviews()
    } catch (err) {
      alert(err.message)
    }
  }

  const handleAddReply = async (reviewId) => {
    const text = replyTexts[reviewId]
    if (!text || !text.trim()) return

    try {
      const res = await fetch(`${API_BASE}/reviews/${reviewId}/replies`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${authToken}` },
        body: JSON.stringify({ reply_text: text })
      })
      if (!res.ok) throw new Error('Reply submission failed')
      setReplyTexts({ ...replyTexts, [reviewId]: '' })
      fetchReviews()
    } catch (err) {
      alert(err.message)
    }
  }

  const handleDeleteReview = async (reviewId) => {
    if (!window.confirm('Delete this review?')) return
    try {
      const res = await fetch(`${API_BASE}/reviews/${reviewId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${authToken}` }
      })
      if (!res.ok) throw new Error('Review deletion failed')
      fetchReviews()
    } catch (err) {
      alert(err.message)
    }
  }

  const handleTargetClick = (type, id) => {
    if (type === 'character' && id) {
      fetchCharacterDetails(id)
    } else if (type === 'team') {
      setActiveTab('teams')
    }
  }

  const isModerator = currentUser?.role === 'moderator'

  return (
    <div className="container">
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        currentUser={currentUser}
        onLogout={handleLogout}
        onOpenAbout={() => setShowAboutModal(true)}
        reviewsCount={reviews.length}
      />

      {activeTab === 'characters' && (
        <CharacterTab
          characters={characters}
          loading={loadingCharacters}
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
          selectedElement={selectedElement}
          setSelectedElement={setSelectedElement}
          selectedWeapon={selectedWeapon}
          setSelectedWeapon={setSelectedWeapon}
          elements={ELEMENTS}
          weaponTypes={WEAPON_TYPES}
          isModerator={isModerator}
          onOpenCreateModal={() => setIsCreatingChar(true)}
          onViewBuilds={fetchCharacterDetails}
          onEditCharacter={(c) => {
            setEditingChar(c)
            setEditDesc(c.description || '')
            setEditRegion(c.region)
          }}
          onDeleteCharacter={handleDeleteCharacter}
        />
      )}

      {activeTab === 'teams' && (
        <TeamTab
          teams={teams}
          loading={loadingTeams}
          isModerator={isModerator}
          onOpenCreateTeam={handleOpenCreateTeam}
          onEditTeam={handleOpenEditTeam}
          onDeleteTeam={handleDeleteTeam}
        />
      )}

      {activeTab === 'reviews' && (
        <ReviewTab
          reviews={reviews}
          loading={loadingReviews}
          currentUser={currentUser}
          newRating={newRating}
          setNewRating={setNewRating}
          newComment={newComment}
          setNewComment={setNewComment}
          refType={refType}
          setRefType={setRefType}
          refId={refId}
          setRefId={setRefId}
          characters={characters}
          teams={teams}
          replyTexts={replyTexts}
          onReplyTextChange={(id, val) => setReplyTexts({ ...replyTexts, [id]: val })}
          onSubmitReview={handleAddReview}
          onAddReply={handleAddReply}
          onDeleteReview={handleDeleteReview}
          onTargetClick={handleTargetClick}
        />
      )}

      <Modals
        showAbout={showAboutModal}
        onCloseAbout={() => setShowAboutModal(false)}
        isCreatingChar={isCreatingChar}
        onCloseCreateChar={() => setIsCreatingChar(false)}
        newCharData={newCharData}
        setNewCharData={setNewCharData}
        onCreateChar={handleCreateCharacter}
        editingChar={editingChar}
        onCloseEditChar={() => setEditingChar(null)}
        editRegion={editRegion}
        setEditRegion={setEditRegion}
        editDesc={editDesc}
        setEditDesc={setEditDesc}
        onSaveEditChar={handleSaveCharacterEdit}
        selectedCharDetails={selectedCharDetails}
        onCloseCharDetails={() => {
          setSelectedCharDetails(null)
          setIsCreatingBuild(false)
          setEditingBuild(null)
        }}
        loadingDetails={loadingDetails}
        isModerator={isModerator}
        isCreatingBuild={isCreatingBuild}
        setIsCreatingBuild={setIsCreatingBuild}
        editingBuild={editingBuild}
        setEditingBuild={setEditingBuild}
        buildForm={buildForm}
        setBuildForm={setBuildForm}
        onSaveBuild={handleSaveBuild}
        onDeleteBuild={handleDeleteBuild}
        teamModalOpen={teamModalOpen}
        onCloseTeamModal={() => setTeamModalOpen(false)}
        editingTeamId={editingTeamId}
        teamForm={teamForm}
        setTeamForm={setTeamForm}
        onSaveTeam={handleSaveTeam}
        characters={characters}
        elements={ELEMENTS}
        weaponTypes={WEAPON_TYPES}
        teamRoles={TEAM_ROLES}
        teamTypes={TEAM_TYPES}
      />
    </div>
  )
}