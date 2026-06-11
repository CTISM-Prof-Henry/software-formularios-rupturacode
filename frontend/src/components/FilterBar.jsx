import { Filter, Search } from 'lucide-react'

function FilterBar({ searchPlaceholder, searchValue, onSearchChange, selects = [], onFilter }) {
  return (
    <form
      className="filter-bar"
      onSubmit={(event) => {
        event.preventDefault()
        if (onFilter) {
          onFilter()
        }
      }}
    >
      <div className="filter-search">
        <Search size={16} />
        <input
          aria-label="Buscar"
          onChange={(event) => onSearchChange(event.target.value)}
          placeholder={searchPlaceholder}
          type="search"
          value={searchValue}
        />
      </div>

      {selects.map((select) => (
        <select
          aria-label={select.label}
          className="filter-select"
          key={select.label}
          onChange={(event) => select.onChange(event.target.value)}
          value={select.value}
        >
          <option value="">{select.label}</option>
          {select.options.map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
      ))}

      <button className="primary-button filter-submit" type="submit">
        <Filter size={16} />
        Filtrar
      </button>
    </form>
  )
}

export default FilterBar
