"use client";

import React from "react";

interface LogoProps {
    className?: string;
    variant?: "dark" | "light";
    showText?: boolean;
}

export function Logo({ className = "", variant = "dark", showText = true }: LogoProps) {
    const textColor = variant === "dark" ? "text-white" : "text-gray-900";

    return (
        <div className={`flex items-center gap-3 ${className}`}>
            <div className="w-10 h-10 rounded-xl flex items-center justify-center shrink-0 shadow-sm border border-white/10 bg-gradient-to-br from-indigo-600 to-purple-600">
                <svg width="26" height="26" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="LearnPulse logo">
                    <defs>
                        <linearGradient id="lp-grad" x1="0" x2="1">
                            <stop offset="0%" stopColor="#FFFFFF" stopOpacity="0.95" />
                            <stop offset="100%" stopColor="#FFFFFF" stopOpacity="0.8" />
                        </linearGradient>
                    </defs>
                    <rect x="4" y="4" width="56" height="56" rx="10" fill="url(#lp-grad)" fillOpacity="0.06" />
                    <path d="M18 44C20 34 26 30 34 30c6 0 10 3 12 8" stroke="#FFFFFF" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
                    <path d="M20 28c6-6 16-6 22 0" stroke="#FFFFFF" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
            </div>

            {showText && (
                <span className={`font-bold text-xl tracking-tight ${textColor}`}>
                    LearnPulse
                </span>
            )}
        </div>
    );
}
