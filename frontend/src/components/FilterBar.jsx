import { Filter, Search } from 'lucide-react'
import SearchableSelect from './SearchableSelect.jsx'

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
        <div className="filter-select" key={select.label}>
          <SearchableSelect
            onChange={select.onChange}
            options={select.options}
            placeholder={select.label}
            searchPlaceholder={`Pesquisar ${select.label.toLowerCase()}`}
            value={select.value}
          />
        </div>
      ))}

      <button className="primary-button filter-submit" type="submit">
        <Filter size={16} />
        Filtrar
      </button>
    </form>
  )
}

export default FilterBar
