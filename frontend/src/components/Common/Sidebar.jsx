import React from 'react';
import { NavLink, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Home, Landmark, Users, LayoutDashboard, Settings, LogOut, ShieldCheck, MapPin, Grid, Heart, Search } from 'lucide-react';

const Sidebar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  const isAdmin = user && user.role === 'admin';
  const isAgent = user && user.role === 'agent';
  const isBuyer = user && user.role === 'buyer';

  return (
    <div className="w-64 bg-slate-900 border-r border-slate-800 text-slate-350 flex flex-col h-full">
      {/* Brand Header */}
      <div className="h-16 flex items-center px-6 border-b border-slate-800">
        <Link to="/" className="flex items-center gap-2">
          <span className="p-1.5 rounded-lg bg-indigo-605 text-white">
            <Home className="h-5 w-5" />
          </span>
          <span className="font-bold text-white text-base">Estate<span className="text-emerald-450">Hub</span></span>
        </Link>
      </div>

      {/* Nav Links */}
      <div className="flex-1 px-4 py-6 space-y-1.5 overflow-y-auto">
        <span className="px-3 text-2xs uppercase tracking-wider font-extrabold text-slate-500 block mb-2">Navigation</span>
        
        <NavLink
          to="/dashboard"
          end
          className={({ isActive }) =>
            `flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold transition-all ${
              isActive ? 'bg-indigo-600 text-white shadow-md shadow-indigo-500/10' : 'hover:bg-slate-800 hover:text-white'
            }`
          }
        >
          <LayoutDashboard className="h-4.5 w-4.5" />
          <span>Overview</span>
        </NavLink>

        {isBuyer && (
          <>
            <NavLink
              to="/favorites"
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold transition-all ${
                  isActive ? 'bg-indigo-600 text-white shadow-md shadow-indigo-500/10' : 'hover:bg-slate-800 hover:text-white'
                }`
              }
            >
              <Heart className="h-4.5 w-4.5" />
              <span>My Favorites</span>
            </NavLink>
            <NavLink
              to="/properties"
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold transition-all ${
                  isActive ? 'bg-indigo-600 text-white shadow-md shadow-indigo-500/10' : 'hover:bg-slate-800 hover:text-white'
                }`
              }
            >
              <Search className="h-4.5 w-4.5" />
              <span>Browse Listings</span>
            </NavLink>
          </>
        )}

        {isAgent && (
          <NavLink
            to="/dashboard"
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold transition-all ${
                isActive ? 'bg-indigo-600 text-white shadow-md shadow-indigo-500/10' : 'hover:bg-slate-800 hover:text-white'
              }`
            }
          >
            <Landmark className="h-4.5 w-4.5" />
            <span>My Properties</span>
          </NavLink>
        )}

        {(isAdmin || isAgent) && (
          <NavLink
            to="/dashboard/locations"
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold transition-all ${
                isActive ? 'bg-indigo-600 text-white shadow-md shadow-indigo-500/10' : 'hover:bg-slate-800 hover:text-white'
              }`
            }
          >
            <MapPin className="h-4.5 w-4.5" />
            <span>Manage Locations</span>
          </NavLink>
        )}

        {isAdmin && (
          <>
            <span className="px-3 text-2xs uppercase tracking-wider font-extrabold text-slate-500 block pt-4 mb-2">Admin Tools</span>
            <NavLink
              to="/dashboard/users"
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold transition-all ${
                  isActive ? 'bg-indigo-600 text-white' : 'hover:bg-slate-800 hover:text-white'
                }`
              }
            >
              <Users className="h-4.5 w-4.5" />
              <span>Manage Users</span>
            </NavLink>
            <NavLink
              to="/dashboard/properties"
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold transition-all ${
                  isActive ? 'bg-indigo-600 text-white' : 'hover:bg-slate-800 hover:text-white'
                }`
              }
            >
              <Landmark className="h-4.5 w-4.5" />
              <span>Manage Listings</span>
            </NavLink>
            <NavLink
              to="/dashboard/amenities"
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold transition-all ${
                  isActive ? 'bg-indigo-600 text-white' : 'hover:bg-slate-800 hover:text-white'
                }`
              }
            >
              <Grid className="h-4.5 w-4.5" />
              <span>Manage Amenities</span>
            </NavLink>

            <NavLink
              to="/dashboard/types"
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold transition-all ${
                  isActive ? 'bg-indigo-600 text-white' : 'hover:bg-slate-800 hover:text-white'
                }`
              }
            >
              <ShieldCheck className="h-4.5 w-4.5" />
              <span>Property Types</span>
            </NavLink>
          </>
        )}
      </div>

      {/* User profile / Logout bottom info */}
      <div className="p-4 border-t border-slate-800 space-y-3">
        <NavLink
          to="/profile"
          className="flex items-center gap-3 p-2.5 rounded-xl hover:bg-slate-800 transition-colors"
        >
          <div className="h-9 w-9 rounded-xl bg-indigo-605 text-white flex items-center justify-center font-extrabold text-sm uppercase">
            {user?.email?.[0] || 'A'}
          </div>
          <div className="flex-1 min-w-0">
            <span className="block text-xs font-bold text-white truncate">{user?.first_name || 'Agent'}</span>
            <span className="block text-2xs text-slate-500 uppercase font-extrabold tracking-wide">{user?.role}</span>
          </div>
        </NavLink>
        
        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold text-rose-450 hover:bg-rose-950/20 hover:text-rose-400 transition-colors cursor-pointer"
        >
          <LogOut className="h-4.5 w-4.5" />
          <span>Sign Out</span>
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
