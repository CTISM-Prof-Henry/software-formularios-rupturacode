import { useMemo, useRef, useState } from 'react'
import { ChevronDown, Search, X } from 'lucide-react'

function normalizeOption(option) {
  if (typeof option === 'string') {
    return { value: option, label: option }
  }
  return {
    value: String(option.value ?? ''),
    label: option.label ?? String(option.value ?? ''),
  }
}

function filterOptions(options, query) {
  const normalizedQuery = query.trim().toLowerCase()
  if (!normalizedQuery) {
    return options
  }
  return options.filter((option) => option.label.toLowerCase().includes(normalizedQuery))
}

function SearchableSelect({
  ariaInvalid,
  disabled = false,
  emptyLabel = 'Nenhuma opcao encontrada',
  onChange,
  options = [],
  placeholder = 'Selecione',
  searchPlaceholder = 'Pesquisar...',
  value = '',
}) {
  const [isOpen, setIsOpen] = useState(false)
  const [query, setQuery] = useState('')
  const closeTimer = useRef(null)

  const normalizedOptions = useMemo(() => options.map(normalizeOption), [options])
  const selected = normalizedOptions.find((option) => option.value === String(value))
  const visibleOptions = useMemo(
    () => filterOptions(normalizedOptions, query),
    [normalizedOptions, query],
  )

  function open() {
    if (!disabled) {
      window.clearTimeout(closeTimer.current)
      setIsOpen(true)
    }
  }

  function close() {
    closeTimer.current = window.setTimeout(() => {
      setIsOpen(false)
      setQuery('')
    }, 120)
  }

  function selectOption(option) {
    onChange(option.value)
    setQuery('')
    setIsOpen(false)
  }

  function clearValue(event) {
    event.preventDefault()
    event.stopPropagation()
    onChange('')
    setQuery('')
    setIsOpen(false)
  }

  return (
    <div
      className={`searchable-select${isOpen ? ' open' : ''}${disabled ? ' disabled' : ''}`}
      data-invalid={ariaInvalid ? 'true' : 'false'}
    >
      <div className="searchable-select-control" onMouseDown={open}>
        <Search size={15} />
        <input
          aria-autocomplete="list"
          aria-expanded={isOpen}
          aria-invalid={ariaInvalid ? 'true' : 'false'}
          autoComplete="off"
          disabled={disabled}
          onBlur={close}
          onChange={(event) => {
            setQuery(event.target.value)
            setIsOpen(true)
          }}
          onFocus={open}
          placeholder={selected ? selected.label : placeholder}
          role="combobox"
          type="search"
          value={isOpen ? query : selected?.label || ''}
        />
        {value ? (
          <button aria-label="Limpar selecao" className="searchable-select-clear" onClick={clearValue} type="button">
            <X size={14} />
          </button>
        ) : null}
        <ChevronDown className="searchable-select-chevron" size={16} />
      </div>

      {isOpen ? (
        <div className="searchable-select-menu" role="listbox">
          <div className="searchable-select-search">{searchPlaceholder}</div>
          {visibleOptions.length ? (
            visibleOptions.map((option) => (
              <button
                aria-selected={option.value === String(value)}
                className="searchable-select-option"
                key={option.value}
                onMouseDown={(event) => {
                  event.preventDefault()
                  selectOption(option)
                }}
                role="option"
                type="button"
              >
                {option.label}
              </button>
            ))
          ) : (
            <div className="searchable-select-empty">{emptyLabel}</div>
          )}
        </div>
      ) : null}
    </div>
  )
}

export default SearchableSelect
