import { useEffect, useRef, useState } from 'react'
import { Check, ChevronDown, Search } from 'lucide-react'

function normalize(options) {
  return options.map((option) =>
    typeof option === 'string' ? { value: option, label: option } : option,
  )
}

function Select({
  ariaInvalid,
  className = '',
  disabled = false,
  onChange,
  options = [],
  placeholder = 'Selecione',
  searchable,
  value,
}) {
  const [open, setOpen] = useState(false)
  const [query, setQuery] = useState('')
  const rootRef = useRef(null)

  const opts = normalize(options)
  const selected = opts.find((option) => String(option.value) === String(value))
  const enableSearch = searchable ?? opts.length > 12

  useEffect(() => {
    if (!open) {
      return undefined
    }

    function handleOutside(event) {
      if (rootRef.current && !rootRef.current.contains(event.target)) {
        setOpen(false)
      }
    }

    function handleKey(event) {
      if (event.key === 'Escape') {
        setOpen(false)
      }
    }

    document.addEventListener('mousedown', handleOutside)
    document.addEventListener('keydown', handleKey)
    return () => {
      document.removeEventListener('mousedown', handleOutside)
      document.removeEventListener('keydown', handleKey)
    }
  }, [open])

  const filtered =
    enableSearch && query
      ? opts.filter((option) => option.label.toLowerCase().includes(query.toLowerCase()))
      : opts

  function pick(nextValue) {
    onChange(nextValue)
    setOpen(false)
    setQuery('')
  }

  return (
    <div
      className={`select ${className} ${open ? 'is-open' : ''} ${disabled ? 'is-disabled' : ''}`}
      ref={rootRef}
    >
      <button
        aria-expanded={open}
        aria-haspopup="listbox"
        aria-invalid={ariaInvalid}
        className="select-control"
        disabled={disabled}
        onClick={() => setOpen((current) => !current)}
        type="button"
      >
        <span className={selected ? 'select-value' : 'select-placeholder'}>
          {selected ? selected.label : placeholder}
        </span>
        <ChevronDown className="select-caret" size={16} />
      </button>

      {open && (
        <div className="select-popup" role="listbox">
          {enableSearch && (
            <div className="select-search">
              <Search size={14} />
              <input
                autoFocus
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Buscar..."
                value={query}
              />
            </div>
          )}

          <ul className="select-options">
            {filtered.length === 0 && <li className="select-empty">Nenhum resultado</li>}
            {filtered.map((option) => {
              const isSelected = String(option.value) === String(value)
              return (
                <li
                  aria-selected={isSelected}
                  className={`select-option ${isSelected ? 'is-selected' : ''}`}
                  key={option.value}
                  onClick={() => pick(option.value)}
                  role="option"
                >
                  <span>{option.label}</span>
                  {isSelected && <Check size={14} />}
                </li>
              )
            })}
          </ul>
        </div>
      )}
    </div>
  )
}

export default Select
