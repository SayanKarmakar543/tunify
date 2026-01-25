const AuthLayout = ({ children }) => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-black">
      <div className="w-full max-w-md p-6 bg-zinc-900 rounded-lg">
        {children}
      </div>
    </div>
  );
};

export default AuthLayout;
