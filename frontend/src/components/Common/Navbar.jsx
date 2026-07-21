import React, { useState } from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useFavorites } from '../../context/FavoriteContext';
import { useTheme } from '../../context/ThemeContext';
import { Home, Heart, Sun, Moon, LayoutDashboard, LogOut, Menu, X, PlusCircle, User } from 'lucide-react';

const Navbar = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const { favorites } = useFavorites();
  const { darkMode, toggleDarkMode } = useTheme();
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  const isAgentOrAdmin = user && ['agent', 'admin'].includes(user.role);

  return (
    <nav className="sticky top-0 z-50 bg-white/70 dark:bg-slate-900/70 backdrop-blur-md border-b border-slate-200/80 dark:border-slate-800 shadow-sm transition-colors duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="shrink-0 flex items-center gap-2">
              <span className="p-2 rounded-xl bg-linear-to-tr from-indigo-650 to-emerald-500 text-white shadow-md shadow-indigo-200">
                <Home className="h-6 w-6" />
              </span>
              <span className="font-extrabold text-xl tracking-tight bg-linear-to-r from-indigo-900 to-indigo-700 dark:from-white dark:to-slate-300 bg-clip-text text-transparent">
                Estate<span className="text-emerald-500 font-black">Hub</span>
              </span>
            </Link>
            
            <div className="hidden md:ml-8 md:flex md:space-x-4">
              <NavLink
                to="/"
                className={({ isActive }) =>
                  `inline-flex items-center px-3 py-2 text-sm font-semibold rounded-lg transition-colors ${
                    isActive ? 'text-indigo-600 dark:text-indigo-400 bg-indigo-50/50 dark:bg-slate-800' : 'text-slate-650 dark:text-slate-350 hover:text-indigo-600 dark:hover:text-indigo-400'
                  }`
                }
              >
                Home
              </NavLink>
              <NavLink
                to="/properties"
                className={({ isActive }) =>
                  `inline-flex items-center px-3 py-2 text-sm font-semibold rounded-lg transition-colors ${
                    isActive ? 'text-indigo-600 dark:text-indigo-400 bg-indigo-50/50 dark:bg-slate-800' : 'text-slate-650 dark:text-slate-350 hover:text-indigo-600 dark:hover:text-indigo-400'
                  }`
                }
              >
                Browse Properties
              </NavLink>
              {isAuthenticated && (
                <NavLink
                  to="/dashboard"
                  className={({ isActive }) =>
                    `inline-flex items-center px-3 py-2 text-sm font-semibold rounded-lg transition-colors ${
                      isActive ? 'text-indigo-600 dark:text-indigo-400 bg-indigo-50/50 dark:bg-slate-800' : 'text-slate-650 dark:text-slate-350 hover:text-indigo-600 dark:hover:text-indigo-400'
                    }`
                  }
                >
                  <LayoutDashboard className="h-4 w-4 mr-1.5" />
                  Dashboard
                </NavLink>
              )}
            </div>
          </div>

          <div className="hidden md:flex items-center space-x-4">
            {/* Theme Toggle Button */}
            <button
              onClick={toggleDarkMode}
              className="p-2 text-slate-500 dark:text-slate-400 hover:text-indigo-600 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors cursor-pointer"
            >
              {darkMode ? <Sun className="h-5.5 w-5.5" /> : <Moon className="h-5.5 w-5.5" />}
            </button>

            <Link
              to="/favorites"
              className="relative p-2 text-slate-500 dark:text-slate-400 hover:text-rose-500 transition-colors rounded-full hover:bg-slate-100 dark:hover:bg-slate-800"
            >
              <Heart className="h-5.5 w-5.5" />
              {favorites.length > 0 && (
                <span className="absolute -top-1 -right-1 bg-rose-500 text-white rounded-full text-2xs w-5 h-5 flex items-center justify-center font-bold shadow-sm animate-pulse">
                  {favorites.length}
                </span>
              )}
            </Link>

            {isAgentOrAdmin && (
              <Link
                to="/dashboard/properties/new"
                className="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-bold text-white bg-indigo-600 hover:bg-indigo-700 transition-colors rounded-xl shadow-md"
              >
                <PlusCircle className="h-4 w-4" />
                List Property
              </Link>
            )}

            {isAuthenticated ? (
              <div className="flex items-center gap-3">
                <Link to="/profile" className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 hover:border-indigo-400 transition-colors">
                  <div className="h-6 w-6 rounded-full bg-indigo-100 dark:bg-indigo-950 flex items-center justify-center text-indigo-700 dark:text-indigo-300 font-bold text-xs uppercase">
                    {user?.first_name?.[0] || <User className="h-3 w-3" />}
                  </div>
                  <span className="text-sm font-semibold text-slate-750 dark:text-slate-250 max-w-25 truncate">{user?.first_name}</span>
                </Link>
                <button
                  onClick={handleLogout}
                  className="p-2 text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white transition-colors hover:bg-slate-100 dark:hover:bg-slate-800 rounded-full"
                  title="Logout"
                >
                  <LogOut className="h-5 w-5" />
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link
                  to="/login"
                  className="px-4 py-2 text-sm font-bold text-slate-700 dark:text-slate-350 hover:text-indigo-600 hover:bg-slate-50 dark:hover:bg-slate-800 rounded-xl transition-all"
                >
                  Sign In
                </Link>
                <Link
                  to="/register"
                  className="px-4 py-2 text-sm font-bold text-indigo-650 bg-indigo-50 dark:bg-indigo-950/40 rounded-xl hover:bg-indigo-100 dark:hover:bg-indigo-950/60 transition-all"
                >
                  Create Account
                </Link>
              </div>
            )}
          </div>

          {/* Mobile menu controllers */}
          <div className="flex items-center md:hidden gap-2">
            <button
              onClick={toggleDarkMode}
              className="p-2 text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-full"
            >
              {darkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
            </button>
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="inline-flex items-center justify-center p-2 rounded-xl text-slate-500 hover:text-slate-900 hover:bg-slate-100 dark:hover:bg-slate-800 focus:outline-none"
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile drop menu */}
      {isOpen && (
        <div className="md:hidden bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 px-4 pt-2 pb-4 space-y-2 shadow-inner">
          <Link
            to="/"
            onClick={() => setIsOpen(false)}
            className="block px-3 py-2 rounded-lg text-base font-semibold text-slate-700 dark:text-slate-300 hover:text-indigo-605"
          >
            Home
          </Link>
          <Link
            to="/properties"
            onClick={() => setIsOpen(false)}
            className="block px-3 py-2 rounded-lg text-base font-semibold text-slate-700 dark:text-slate-300 hover:text-indigo-605"
          >
            Browse Properties
          </Link>
          {isAuthenticated && (
            <Link
              to="/dashboard"
              onClick={() => setIsOpen(false)}
              className="block px-3 py-2 rounded-lg text-base font-semibold text-slate-705 dark:text-slate-300 hover:text-indigo-605"
            >
              Dashboard
            </Link>
          )}
          {isAgentOrAdmin && (
            <Link
              to="/dashboard/properties/new"
              onClick={() => setIsOpen(false)}
              className="block px-3 py-2 rounded-lg text-base font-semibold text-slate-705 dark:text-slate-300 hover:text-indigo-605"
            >
              List Property
            </Link>
          )}
          <hr className="border-slate-100 dark:border-slate-800 my-2" />
          {isAuthenticated ? (
            <div className="space-y-2 pt-2">
              <Link
                to="/profile"
                onClick={() => setIsOpen(false)}
                className="block px-3 py-2 rounded-lg text-base font-semibold text-slate-750 dark:text-slate-250 hover:bg-slate-50 dark:hover:bg-slate-800"
              >
                Profile & Settings
              </Link>
              <button
                onClick={() => {
                  setIsOpen(false);
                  handleLogout();
                }}
                className="w-full text-left flex items-center gap-2 px-3 py-2 rounded-lg text-base font-semibold text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/20"
              >
                <LogOut className="h-5 w-5" />
                Sign Out
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-2 gap-2 pt-2">
              <Link
                to="/login"
                onClick={() => setIsOpen(false)}
                className="text-center px-4 py-2 text-sm font-semibold text-slate-705 border border-slate-200 dark:border-slate-700 dark:text-slate-300 rounded-lg"
              >
                Sign In
              </Link>
              <Link
                to="/register"
                onClick={() => setIsOpen(false)}
                className="text-center px-4 py-2 text-sm font-semibold text-white bg-indigo-600 rounded-lg"
              >
                Sign Up
              </Link>
            </div>
          )}
        </div>
      )}
    </nav>
  );
};

export default Navbar;
