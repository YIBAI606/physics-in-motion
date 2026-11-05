// Pure time functions: no accumulated frame state or random numbers.
export const clamp = x => Math.max(0, Math.min(1, x));
export const ease = x => { x = clamp(x); return x*x*(3-2*x); };
export const reveal = (t, start=0, duration=.6) => duration>0 ? ease((t-start)/duration) : +(t>=start);
export const lerp = (a,b,p) => a+(b-a)*p;
export const arrowHead = (t,start,duration,x0,x1) => lerp(x0,x1,reveal(t,start,duration));
// Looping decorative motion must never be interpreted as a simulation.
