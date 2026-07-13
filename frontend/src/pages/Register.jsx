import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useNotifications } from '../context/NotificationContext';
import RegisterForm from '../components/Auth/RegisterForm';
import { UserPlus } from 'lucide-react';

const Register = () => {
  const { register: signup } = useAuth();
  const { showSuccess, showError } = useNotifications();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const onSubmit = async (data) => {
    setLoading(true);
    try {
      const userData = await signup(data);
      showSuccess('Registration complete!');
      navigate(userData?.role === 'buyer' ? '/profile' : '/dashboard');
    } catch (err) {
      showError(err.response?.data?.message || 'Registration failed. Email might already exist.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[85vh] flex items-center justify-center bg-slate-50 dark:bg-slate-950 px-4 py-12">
      <div className="max-w-md w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-8 rounded-3xl shadow-xl space-y-6">
        <div className="text-center space-y-2">
          <div className="inline-flex p-3 rounded-2xl bg-indigo-50 dark:bg-indigo-950/40 text-indigo-605 mb-1 border border-indigo-100 dark:border-indigo-900">
            <UserPlus className="h-6 w-6" />
          </div>
          <h2 className="text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight">Create Account</h2>
          <p className="text-slate-505 dark:text-slate-400 text-sm">Join us to list properties or save favorites.</p>
        </div>

        <RegisterForm onSubmit={onSubmit} loading={loading} />

        <div className="text-center pt-2 text-xs text-slate-500 font-medium">
          Already have an account?{' '}
          <Link to="/login" className="text-indigo-650 hover:underline font-bold">
            Sign in
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Register;
