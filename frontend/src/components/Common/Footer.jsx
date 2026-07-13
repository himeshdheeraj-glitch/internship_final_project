import React from 'react';
import { Home, Mail, Phone, MapPin, Globe } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-slate-900 text-slate-300 border-t border-slate-800">
      <div className="max-w-7xl mx-auto px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <span className="p-1.5 rounded-lg bg-indigo-600 text-white">
                <Home className="h-5 w-5" />
              </span>
              <span className="font-bold text-lg text-white">
                Estate<span className="text-emerald-400">Hub</span>
              </span>
            </div>
            <p className="text-sm text-slate-400">
              Discover beautiful homes, luxury apartments, and premium land plots. We make finding your dream property stress-free and seamless.
            </p>
          </div>
          
          <div>
            <h3 className="text-white font-semibold mb-4 text-sm uppercase tracking-wider">Quick Links</h3>
            <ul className="space-y-2 text-sm text-slate-400">
              <li><a href="/" className="hover:text-emerald-400 transition-colors">Home</a></li>
              <li><a href="/properties" className="hover:text-emerald-400 transition-colors">Properties</a></li>
              <li><a href="/favorites" className="hover:text-emerald-400 transition-colors">Favorites</a></li>
              <li><a href="/login" className="hover:text-emerald-400 transition-colors">Agent Portal</a></li>
            </ul>
          </div>

          <div>
            <h3 className="text-white font-semibold mb-4 text-sm uppercase tracking-wider">Legal</h3>
            <ul className="space-y-2 text-sm text-slate-400">
              <li><span className="hover:text-emerald-400 transition-colors cursor-pointer">Privacy Policy</span></li>
              <li><span className="hover:text-emerald-400 transition-colors cursor-pointer">Terms of Service</span></li>
              <li><span className="hover:text-emerald-400 transition-colors cursor-pointer">Cookie Policy</span></li>
            </ul>
          </div>

          <div className="space-y-3">
            <h3 className="text-white font-semibold mb-4 text-sm uppercase tracking-wider">Contact Info</h3>
            <div className="flex items-center gap-2 text-sm text-slate-400">
              <MapPin className="h-4 w-4 text-emerald-400 shrink-0" />
              <span>123 Estate Hub Avenue, Downtown</span>
            </div>
            <div className="flex items-center gap-2 text-sm text-slate-400">
              <Phone className="h-4 w-4 text-emerald-400 shrink-0" />
              <span>+1 (555) 010-2026</span>
            </div>
            <div className="flex items-center gap-2 text-sm text-slate-400">
              <Mail className="h-4 w-4 text-emerald-400 shrink-0" />
              <span>support@estatehub.com</span>
            </div>
          </div>
        </div>
        
        <div className="border-t border-slate-800 mt-12 pt-6 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-4">
          <p>© 2026 Estate Hub. All rights reserved.</p>
          <div className="flex gap-4">
            <a href="#" className="hover:text-slate-300"><Globe className="h-4 w-4" /></a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
