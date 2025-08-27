import { Card, Text, Group, Badge, Anchor } from '@mantine/core';
import { IconExternalLink, IconCalendar } from '@tabler/icons-react';
import { SearchResult } from '../types/search';

interface ResultItemProps {
  result: SearchResult;
}

export const ResultItem = ({ result }: ResultItemProps) => {
  const formatDate = (dateString?: string) => {
    if (!dateString) return null;
    return new Date(dateString).toLocaleDateString('ja-JP');
  };

  return (
    <Card shadow="sm" padding="lg" radius="md" withBorder>
      <Group justify="space-between" mb="xs">
        <Text fw={500} size="lg" lineClamp={2}>
          <Anchor href={result.url} target="_blank" rel="noopener noreferrer">
            {result.title}
          </Anchor>
        </Text>
        <Badge color="blue" variant="light">
          {Math.round(result.score * 100)}%
        </Badge>
      </Group>

      <Text size="sm" c="dimmed" mb="md" lineClamp={3}>
        {result.description}
      </Text>

      <Group gap="xs" justify="space-between">
        <Group gap="xs">
          <IconExternalLink size={14} />
          <Text size="xs" c="dimmed" style={{ wordBreak: 'break-all' }}>
            {result.url}
          </Text>
        </Group>
        
        {result.publishedAt && (
          <Group gap="xs">
            <IconCalendar size={14} />
            <Text size="xs" c="dimmed">
              {formatDate(result.publishedAt)}
            </Text>
          </Group>
        )}
      </Group>
    </Card>
  );
};
