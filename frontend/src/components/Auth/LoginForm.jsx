import React from 'react';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { Mail, Lock, LogIn } from 'lucide-react';

const schema = yup.object().shape({
  email: yup.string().email('Invalid email').required('Email is required'),
  password: yup.string().min(6, 'Password is too short').required('Password is required')
});

const LoginForm = ({ onSubmit, loading = false }) => {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: yupResolver(schema)
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div className="space-y-1">
        <label className="block text-xs font-bold text-slate-500 dark:text-slate-400 uppercase">Email Address</label>
        <div className="relative">
          <span className="absolute inset-y-0 left-0 pl-3 flex items-center text-slate-400">
            <Mail className="h-4.5 w-4.5" />
          </span>
          <input
            type="email"
            {...register('email')}
            placeholder="e.g. agent@realestate.com"
            className="w-full pl-10 pr-3 py-2.5 bg-slate-50 dark:bg-slate-900 border border-slate-205 dark:border-slate-800 rounded-xl text-sm focus:outline-none focus:border-indigo-400"
          />
        </div>
        {errors.email && <span className="text-xs text-rose-500">{errors.email.message}</span>}
      </div>

      <div className="space-y-1">
        <label className="block text-xs font-bold text-slate-500 dark:text-slate-400 uppercase">Password</label>
        <div className="relative">
          <span className="absolute inset-y-0 left-0 pl-3 flex items-center text-slate-400">
            <Lock className="h-4.5 w-4.5" />
          </span>
          <input
            type="password"
            {...register('password')}
            placeholder="••••••••"
            className="w-full pl-10 pr-3 py-2.5 bg-slate-50 dark:bg-slate-900 border border-slate-205 dark:border-slate-800 rounded-xl text-sm focus:outline-none focus:border-indigo-400"
          />
        </div>
        {errors.password && <span className="text-xs text-rose-500">{errors.password.message}</span>}
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full py-3 bg-indigo-650 hover:bg-indigo-700 text-white font-bold rounded-2xl shadow-md transition-colors disabled:opacity-50 flex items-center justify-center gap-2 cursor-pointer text-sm"
      >
        <LogIn className="h-4 w-4" />
        <span>{loading ? 'Signing In...' : 'Sign In'}</span>
      </button>
    </form>
  );
};

export default LoginForm;
