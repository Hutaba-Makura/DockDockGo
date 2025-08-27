import { Container, Title, Stack, Space } from '@mantine/core';
import { SearchForm } from '../components/SearchForm';
import { ResultList } from '../components/ResultList';
import { useSearch } from '../hooks/useSearch';
import { SearchQuery } from '../types/search';

export const SearchPage = () => {
  const { searchResults, loading, error, search } = useSearch();

  const handleSearch = (query: SearchQuery) => {
    search(query);
  };

  const handlePageChange = (page: number) => {
    if (searchResults) {
      search({
        query: searchResults.query,
        page,
        limit: searchResults.limit,
      });
    }
  };

  return (
    <Container size="lg" py="xl">
      <Stack gap="xl">
        <div>
          <Title order={1} ta="center" mb="md">
            DockDockGo
          </Title>
          <Title order={3} ta="center" c="dimmed" fw={400}>
            検索サイト
          </Title>
        </div>

        <SearchForm onSearch={handleSearch} loading={loading} />

        <Space h="md" />

        <ResultList
          searchResponse={searchResults}
          loading={loading}
          error={error}
          onPageChange={handlePageChange}
        />
      </Stack>
    </Container>
  );
};
