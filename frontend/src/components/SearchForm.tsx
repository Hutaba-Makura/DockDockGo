import { useState } from 'react';
import { TextInput, Button, Group, Paper } from '@mantine/core';
import { IconSearch } from '@tabler/icons-react';
import { SearchQuery } from '../types/search';

interface SearchFormProps {
  onSearch: (query: SearchQuery) => void;
  loading: boolean;
}

export const SearchForm = ({ onSearch, loading }: SearchFormProps) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch({ query: query.trim() });
    }
  };

  return (
    <Paper shadow="sm" p="md" withBorder>
      <form onSubmit={handleSubmit}>
        <Group gap="md" align="flex-end">
          <TextInput
            placeholder="検索したいキーワードを入力してください..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            style={{ flex: 1 }}
            leftSection={<IconSearch size={16} />}
            disabled={loading}
          />
          <Button
            type="submit"
            loading={loading}
            disabled={!query.trim()}
            leftSection={<IconSearch size={16} />}
          >
            検索
          </Button>
        </Group>
      </form>
    </Paper>
  );
};
