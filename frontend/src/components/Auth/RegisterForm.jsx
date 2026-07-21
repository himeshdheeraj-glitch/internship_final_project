import React from 'react';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { Mail, Lock, User, UserPlus, Phone } from 'lucide-react';

const schema = yup.object().shape({
  first_name: yup.string().required('First name is required'),
  last_name: yup.string().required('Last name is required'),
  email: yup.string().email('Invalid email').required('Email is required'),
  phone_number: yup.string().max(20, 'Phone number must be at most 20 characters').required('Phone number is required'),
  password: yup
    .string()
    .min(8, 'Password must be at least 8 characters')
    .matches(/\d/, 'Password must contain at least one digit')
    .matches(/[a-z]/, 'Password must contain at least one lowercase letter')
    .matches(/[A-Z]/, 'Password must contain at least one uppercase letter')
    .matches(/[!@#$%^&*(),.?":{}|<>]/, 'Password must contain at least one special character')
    .required('Password is required'),
  role: yup.string().required('Please select a role')
});

const RegisterForm = ({ onSubmit, loading = false }) => {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: yupResolver(schema)
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-1">
          <label className="block text-xs font-bold text-slate-500 uppercase">First Name</label>
          <input
            type="text"
            {...register('first_name')}
            placeholder="John"
            className="w-full px-3 py-2.5 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none focus:border-indigo-400"
          />
          {errors.first_name && <span className="text-xs text-rose-500">{errors.first_name.message}</span>}
        </div>
        <div className="space-y-1">
          <label className="block text-xs font-bold text-slate-500 uppercase">Last Name</label>
          <input
            type="text"
            {...register('last_name')}
            placeholder="Doe"
            className="w-full px-3 py-2.5 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none focus:border-indigo-400"
          />
          {errors.last_name && <span className="text-xs text-rose-500">{errors.last_name.message}</span>}
        </div>
      </div>

      <div className="space-y-1">
        <label className="block text-xs font-bold text-slate-500 uppercase">Email Address</label>
        <div className="relative">
          <span className="absolute inset-y-0 left-0 pl-3 flex items-center text-slate-400">
            <Mail className="h-4.5 w-4.5" />
          </span>
          <input
            type="email"
            {...register('email')}
            placeholder="e.g. buyer@realestate.com"
            className="w-full pl-10 pr-3 py-2.5 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none focus:border-indigo-400"
          />
        </div>
        {errors.email && <span className="text-xs text-rose-500">{errors.email.message}</span>}
      </div>

      <div className="space-y-1">
        <label className="block text-xs font-bold text-slate-500 uppercase">Mobile Number</label>
        <div className="relative">
          <span className="absolute inset-y-0 left-0 pl-3 flex items-center text-slate-400">
            <Phone className="h-4.5 w-4.5" />
          </span>
          <input
            type="text"
            {...register('phone_number')}
            placeholder="e.g. +1 555-0199"
            className="w-full pl-10 pr-3 py-2.5 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none focus:border-indigo-400"
          />
        </div>
        {errors.phone_number && <span className="text-xs text-rose-500">{errors.phone_number.message}</span>}
      </div>

      <div className="space-y-1">
        <label className="block text-xs font-bold text-slate-500 uppercase">Password</label>
        <div className="relative">
          <span className="absolute inset-y-0 left-0 pl-3 flex items-center text-slate-400">
            <Lock className="h-4.5 w-4.5" />
          </span>
          <input
            type="password"
            {...register('password')}
            placeholder="Min 8 characters"
            className="w-full pl-10 pr-3 py-2.5 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none focus:border-indigo-400"
          />
        </div>
        {errors.password && <span className="text-xs text-rose-500">{errors.password.message}</span>}
      </div>

      <div className="space-y-1">
        <label className="block text-xs font-bold text-slate-500 uppercase">Role</label>
        <select
          {...register('role')}
          className="w-full px-3 py-2.5 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-sm focus:outline-none focus:border-indigo-400"
        >
          <option value="buyer">Buyer (Search & Save Properties)</option>
          <option value="agent">Agent (Publish & Manage Listings)</option>
          <option value="admin">Admin (Platform Manager)</option>
        </select>
        {errors.role && <span className="text-xs text-rose-500">{errors.role.message}</span>}
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full py-3 bg-indigo-650 hover:bg-indigo-700 text-white font-bold rounded-2xl shadow-md transition-colors disabled:opacity-50 flex items-center justify-center gap-2 cursor-pointer text-sm"
      >
        <UserPlus className="h-4.5 w-4.5" />
        <span>{loading ? 'Creating Account...' : 'Sign Up'}</span>
      </button>
    </form>
  );
};

export default RegisterForm;
