import { Stack, Text, Alert, Pagination, Group } from '@mantine/core';
import { IconAlertCircle, IconSearch } from '@tabler/icons-react';
import { SearchResponse } from '../types/search';
import { ResultItem } from './ResultItem';

interface ResultListProps {
  searchResponse: SearchResponse | null;
  loading: boolean;
  error: string | null;
  onPageChange?: (page: number) => void;
}

export const ResultList = ({ 
  searchResponse, 
  loading, 
  error, 
  onPageChange 
}: ResultListProps) => {
  if (loading) {
    return (
      <Stack gap="md">
        {Array.from({ length: 3 }).map((_, index) => (
          <div key={index} style={{ height: 120, background: '#f8f9fa', borderRadius: 8 }} />
        ))}
      </Stack>
    );
  }

  if (error) {
    return (
      <Alert icon={<IconAlertCircle size={16} />} title="エラー" color="red">
        {error}
      </Alert>
    );
  }

  if (!searchResponse) {
    return (
      <Alert icon={<IconSearch size={16} />} title="検索を開始してください" color="blue">
        キーワードを入力して検索ボタンを押してください。
      </Alert>
    );
  }

  if (searchResponse.results.length === 0) {
    return (
      <Alert icon={<IconSearch size={16} />} title="検索結果が見つかりませんでした" color="yellow">
       別のキーワードで検索してみてください。
      </Alert>
    );
  }

  const totalPages = Math.ceil(searchResponse.total / searchResponse.limit);

  return (
    <Stack gap="md">
      <Text size="sm" c="dimmed">
        「{searchResponse.query}」の検索結果: {searchResponse.total}件
      </Text>
      
      <Stack gap="md">
        {searchResponse.results.map((result) => (
          <ResultItem key={result.id} result={result} />
        ))}
      </Stack>

      {totalPages > 1 && (
        <Group justify="center" mt="lg">
          <Pagination
            total={totalPages}
            value={searchResponse.page}
            onChange={onPageChange}
            size="sm"
          />
        </Group>
      )}
    </Stack>
  );
};
