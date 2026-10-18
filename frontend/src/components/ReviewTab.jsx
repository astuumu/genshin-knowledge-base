import ReviewItem from './ReviewItem'

export default function ReviewTab({
  reviews,
  loading,
  currentUser,
  newRating,
  setNewRating,
  newComment,
  setNewComment,
  refType,
  setRefType,
  refId,
  setRefId,
  characters,
  teams,
  replyTexts,
  onReplyTextChange,
  onSubmitReview,
  onAddReply,
  onDeleteReview,
  onTargetClick
}) {
  return (
    <div className="reviews-view">
      {currentUser ? (
        <div className="review-box">
          <h3>Leave a Review or Tactical Tip</h3>
          <div className="review-form-top">
            <div className="rating-select">
              <label>Rating:</label>
              <select
                value={newRating}
                onChange={(e) => setNewRating(Number(e.target.value))}
                className="search-input rating-input"
              >
                <option value={5}>⭐⭐⭐⭐⭐ (5 / 5)</option>
                <option value={4}>⭐⭐⭐⭐ (4 / 5)</option>
                <option value={3}>⭐⭐⭐ (3 / 5)</option>
                <option value={2}>⭐⭐ (2 / 5)</option>
                <option value={1}>⭐ (1 / 5)</option>
              </select>
            </div>

            <div className="ref-selector-group">
              <label>Link to:</label>
              <select
                value={refType}
                onChange={(e) => {
                  setRefType(e.target.value)
                  setRefId('')
                }}
                className="search-input"
              >
                <option value="none">None (General)</option>
                <option value="character">Character / Build</option>
                <option value="team">Team Composition</option>
              </select>

              {refType === 'character' && (
                <select
                  value={refId}
                  onChange={(e) => setRefId(e.target.value)}
                  className="search-input"
                >
                  <option value="">-- Choose Character --</option>
                  {characters.map((c) => (
                    <option key={c.id} value={c.id}>{c.name}</option>
                  ))}
                </select>
              )}

              {refType === 'team' && (
                <select
                  value={refId}
                  onChange={(e) => setRefId(e.target.value)}
                  className="search-input"
                >
                  <option value="">-- Choose Team --</option>
                  {teams.map((t) => (
                    <option key={t.id} value={t.id}>{t.name}</option>
                  ))}
                </select>
              )}
            </div>
          </div>

          <textarea
            rows={3}
            placeholder="Share your thoughts, recommendations, weapon alternatives, or rotation tips..."
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            className="search-input"
          />
          <button className="save-btn" onClick={onSubmitReview}>Submit Review</button>
        </div>
      ) : (
        <div className="login-prompt">
          <p>🔒 Please sign in with your Google account above to leave a review or join discussion threads.</p>
        </div>
      )}

      {loading ? (
        <p className="status-text">Loading community reviews...</p>
      ) : (
        <div className="reviews-list">
          {reviews.map((rev) => (
            <ReviewItem
              key={rev.id}
              review={rev}
              currentUser={currentUser}
              replyText={replyTexts[rev.id]}
              onReplyTextChange={onReplyTextChange}
              onAddReply={onAddReply}
              onDeleteReview={onDeleteReview}
              onTargetClick={onTargetClick}
            />
          ))}
          {reviews.length === 0 && (
            <p className="status-text">No reviews yet. Be the first to share your thoughts!</p>
          )}
        </div>
      )}
    </div>
  )
}