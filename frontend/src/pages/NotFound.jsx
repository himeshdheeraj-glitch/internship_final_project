import React from 'react';
import { Link } from 'react-router-dom';
import { Home } from 'lucide-react';

const NotFound = () => {
  return (
    <div className="min-h-[75vh] flex flex-col items-center justify-center p-4 text-center space-y-6">
      <h1 className="text-6xl font-black text-indigo-650 tracking-wider">404</h1>
      <h2 className="text-xl font-bold text-slate-800">Page Not Found</h2>
      <p className="text-slate-500 text-sm max-w-md">
        The URL path you entered does not exist or may have been moved.
      </p>
      <Link to="/" className="inline-flex items-center gap-2 px-5 py-2.5 bg-indigo-650 hover:bg-indigo-700 text-white font-bold rounded-xl shadow-md text-sm">
        <Home className="h-4.5 w-4.5" />
        <span>Return to Home</span>
      </Link>
    </div>
  );
};

export default NotFound;
