import { useEffect } from "react";

const Modal = ({ isOpen, onClose, title, message }) => {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "unset";
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center backdrop-blur-sm bg-black/50">
      <div
        className="p-6 rounded-2xl shadow-2xl transform transition-all duration-300 scale-100 animate-fadeIn w-full max-w-md primary_object"
        role="dialog"
        aria-modal="true"
      >
        <h2 className="text-2xl font-semibold mb-3 primary_text">{title}</h2>
        <p className="text-gray-700 secondary_text">{message}</p>
        <div className="mt-6 text-right">
          <button
            onClick={onClose}
            className="px-5 py-2 bg-gradient-to-r font-medium rounded-lg hover:opacity-90 shadow primary_button"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default Modal;