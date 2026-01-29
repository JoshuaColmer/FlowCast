export function AnimatedBackground() {
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
      {/* Purple orb - top left */}
      <div
        className="gradient-orb gradient-orb-purple animate-float-slow"
        style={{
          width: '600px',
          height: '600px',
          top: '-10%',
          left: '-10%',
        }}
      />

      {/* Cyan orb - bottom right */}
      <div
        className="gradient-orb gradient-orb-cyan animate-float-medium"
        style={{
          width: '500px',
          height: '500px',
          bottom: '-5%',
          right: '-5%',
          animationDelay: '-5s',
        }}
      />

      {/* Pink orb - center right */}
      <div
        className="gradient-orb gradient-orb-pink animate-float-fast"
        style={{
          width: '400px',
          height: '400px',
          top: '40%',
          right: '10%',
          animationDelay: '-10s',
        }}
      />
    </div>
  );
}
