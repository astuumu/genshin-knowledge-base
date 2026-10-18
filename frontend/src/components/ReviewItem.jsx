export default function ReviewItem({
  review,
  currentUser,
  replyText,
  onReplyTextChange,
  onAddReply,
  onDeleteReview,
  onTargetClick
}) {
  return (
    <div className="review-item">
      <div className="review-item-header">
        <div>
          <strong>👤 {review.user?.username || 'User'}</strong>
          <span className="review-stars">{'★'.repeat(review.rating)}{'☆'.repeat(5 - review.rating)}</span>

          {review.target_type && review.target_type !== 'none' && review.target_name && (
            <span 
              className="ref-badge"
              onClick={() => onTargetClick(review.target_type, review.target_id)}
              title="Click to view details"
            >
              🔗 {review.target_type === 'character' ? 'Character' : 'Team'}: {review.target_name}
            </span>
          )}
        </div>

        {currentUser?.role === 'moderator' && (
          <button className="delete-btn-sm" onClick={() => onDeleteReview(review.id)}>
            🗑️ Delete Review
          </button>
        )}
      </div>

      <p className="review-text">{review.comment}</p>

      <div className="replies-thread">
        {review.replies?.map((reply) => (
          <div key={reply.id} className="reply-bubble">
            <span className="reply-author">
              {reply.user?.role === 'moderator' ? '🛡️ Moderator' : '💬 Member'} ({reply.user?.username}):
            </span>
            <p>{reply.reply_text}</p>
          </div>
        ))}

        {currentUser && (
          <div className="reply-input-row">
            <input
              type="text"
              placeholder="Write a reply..."
              value={replyText || ''}
              onChange={(e) => onReplyTextChange(review.id, e.target.value)}
              className="search-input"
            />
            <button className="reply-btn" onClick={() => onAddReply(review.id)}>Reply</button>
          </div>
        )}
      </div>
    </div>
  )
}