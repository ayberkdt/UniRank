import React from 'react';

export default function Background() {
  return (
    <div className="fixed inset-0 z-[-1] overflow-hidden pointer-events-none bg-[#0a0c10]">
      <div className="absolute top-[-20%] left-[-10%] w-[50vw] h-[50vw] bg-[#6366f1] opacity-[0.15] rounded-full mix-blend-screen filter blur-[100px] animate-[pulse_8s_ease-in-out_infinite]" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[60vw] h-[60vw] bg-[#a855f7] opacity-[0.1] rounded-full mix-blend-screen filter blur-[120px] animate-[pulse_10s_ease-in-out_infinite_reverse]" />
      <div className="absolute top-[30%] left-[40%] w-[40vw] h-[40vw] bg-[#3b82f6] opacity-[0.08] rounded-full mix-blend-screen filter blur-[90px] animate-[pulse_12s_ease-in-out_infinite]" />
    </div>
  );
}
