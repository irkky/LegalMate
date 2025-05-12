import React from 'react';
import { useSpring, animated } from '@react-spring/web';
import { FiGithub, FiLinkedin, FiMail } from 'react-icons/fi';

const Footer = () => {
  const springs = useSpring({
    from: { opacity: 0 },
    to: { opacity: 1 },
    config: { duration: 1000 }
  });

  // Background animation
  const bgAnimation = useSpring({
    from: { backgroundPosition: '0% 50%' },
    to: { backgroundPosition: '100% 50%' },
    config: { duration: 15000 },
    loop: true,
  });

  return (
    <animated.footer 
      style={{
        ...springs,
        background: 'linear-gradient(135deg, #f0f4ff 0%, #f8f0ff 100%)',
        backgroundSize: '200% 200%',
        ...bgAnimation
      }}
      className="border-t border-gray-200 mt-16 flex items-center justify-center min-h-[50vh] relative overflow-hidden"
    >
      {/* Animated background elements */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute w-64 h-64 bg-purple-200 rounded-full -top-32 -left-32 animate-pulse" />
        <div className="absolute w-48 h-48 bg-blue-200 rounded-full top-1/2 right-0 animate-pulse delay-1000" />
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 w-full relative z-10">
        <div className="flex flex-col items-center justify-center text-center">
          {/* Company Section with glassmorphism effect */}
          <div className="max-w-2xl mb-12 backdrop-blur-lg bg-white/50 p-8 rounded-2xl shadow-lg">
            <h5 className="text-2xl font-semibold mb-4 text-gray-900 bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              Contact Us:
            </h5>
            <p className="text-gray-700 text-sm mb-4">
            Ajitesh Kumar: +91 9876543210
            <br/>
            Ratan Kumar: +91-9565334169
            <br/>
            Rishabh Kannaujiya: +91-9264925693
            </p>
            <div className="flex space-x-5 justify-center">
              {[
                { icon: FiGithub, href: 'https://github.com' },
                { icon: FiLinkedin, href: 'https://linkedin.com' },
                { icon: FiMail, href: 'mailto:rishabhkrkannaujiya@gmail.com' }
              ].map((item, index) => (
                <a
                  key={index}
                  href={item.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="p-3 hover:bg-purple-100 rounded-full transition-all duration-300 transform hover:scale-110"
                >
                  <item.icon className="text-gray-600 hover:text-purple-600 w-6 h-6" />
                </a>
              ))}
            </div>
          </div>

          {/* Copyright Section */}
          <div className="border-t border-gray-200 pt-8 w-full max-w-2xl backdrop-blur-sm bg-white/30">
            <p className="text-sm text-gray-600 font-medium">
              © {new Date().getFullYear()} LegalMate. All rights reserved.
            </p>
            <p className="text-xs text-gray-500 mt-2">
              Built with by Group-Id: 04 of Major Project 2025, REC Bijnor.
            </p>
          </div>
        </div>
      </div>
    </animated.footer>
  );
};

export default Footer;