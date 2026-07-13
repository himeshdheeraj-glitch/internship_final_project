import React, { useState, useEffect } from 'react';
import { reviewsService } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { useNotifications } from '../../context/NotificationContext';
import { Star, Trash2 } from 'lucide-react';

const PropertyReviews = ({ propertyId }) => {
  const { user, isAuthenticated } = useAuth();
  const { showSuccess, showError } = useNotifications();
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);

  const [newReview, setNewReview] = useState({ rating: 5, comment: '' });

  const loadReviews = async () => {
    try {
      const list = await reviewsService.getPropertyReviews(propertyId);
      setReviews(list || []);
    } catch (e) {
      console.warn('Failed to load reviews.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadReviews();
  }, [propertyId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!newReview.comment.trim()) {
      showError('Please write a comment.');
      return;
    }
    try {
      await reviewsService.createReview({
        property_id: propertyId,
        rating: newReview.rating,
        comment: newReview.comment
      });
      showSuccess('Review submitted!');
      setNewReview({ rating: 5, comment: '' });
      loadReviews();
    } catch (err) {
      showError('Failed to submit review.');
    }
  };

  const handleDelete = async (reviewId) => {
    if (window.confirm('Delete this review?')) {
      try {
        await reviewsService.deleteReview(reviewId);
        showSuccess('Review deleted.');
        loadReviews();
      } catch (err) {
        showError('Failed to delete review.');
      }
    }
  };

  return (
    <div className="space-y-6 bg-white dark:bg-slate-900 rounded-3xl p-6 border border-slate-200 dark:border-slate-800">
      <h3 className="text-lg font-bold text-slate-800 dark:text-slate-100">Reviews & Ratings</h3>

      {isAuthenticated && (
        <form onSubmit={handleSubmit} className="space-y-4 pb-4 border-b border-slate-100 dark:border-slate-800">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold text-slate-500 uppercase">Rating:</span>
            <div className="flex gap-1">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  type="button"
                  onClick={() => setNewReview({ ...newReview, rating: star })}
                  className="text-amber-400 hover:scale-110 transition-transform cursor-pointer"
                >
                  <Star className={`h-5 w-5 ${newReview.rating >= star ? 'fill-current' : ''}`} />
                </button>
              ))}
            </div>
          </div>
          <div className="space-y-2">
            <textarea
              rows={3}
              placeholder="Share your experience or thoughts on this property..."
              value={newReview.comment}
              onChange={(e) => setNewReview({ ...newReview, comment: e.target.value })}
              className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-850 rounded-xl text-sm focus:outline-none focus:border-indigo-400"
            />
            <button type="submit" className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg text-xs shadow-md">
              Submit Review
            </button>
          </div>
        </form>
      )}

      {loading ? (
        <div className="animate-pulse h-12 bg-slate-100 rounded-xl" />
      ) : reviews.length === 0 ? (
        <p className="text-xs text-slate-450 dark:text-slate-500 font-semibold uppercase">No reviews yet. Be the first to review!</p>
      ) : (
        <div className="space-y-4">
          {reviews.map((rev) => (
            <div key={rev.id} className="flex justify-between items-start gap-4 p-3 bg-slate-50 dark:bg-slate-950/30 rounded-2xl border border-slate-100 dark:border-slate-850">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="font-bold text-sm text-slate-800 dark:text-slate-200">{rev.user?.first_name || 'Visitor'}</span>
                  <div className="flex text-amber-400">
                    {Array.from({ length: rev.rating }).map((_, i) => (
                      <Star key={i} className="h-3.5 w-3.5 fill-current" />
                    ))}
                  </div>
                </div>
                <p className="text-slate-600 dark:text-slate-400 text-xs">{rev.comment}</p>
              </div>
              {(user?.id === rev.user_id || user?.role === 'admin') && (
                <button onClick={() => handleDelete(rev.id)} className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg">
                  <Trash2 className="h-4.5 w-4.5" />
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default PropertyReviews;
