import { useState } from 'react'
import { Eye, EyeOff } from 'lucide-react'

function PasswordInput({ placeholder = '****', ...props }) {
  const [visible, setVisible] = useState(false)

  return (
    <div className="password-input">
      <input placeholder={placeholder} type={visible ? 'text' : 'password'} {...props} />
      <button
        aria-label={visible ? 'Ocultar senha' : 'Mostrar senha'}
        className="password-toggle"
        onClick={() => setVisible((value) => !value)}
        type="button"
      >
        {visible ? <EyeOff size={18} /> : <Eye size={18} />}
      </button>
    </div>
  )
}

export default PasswordInput
