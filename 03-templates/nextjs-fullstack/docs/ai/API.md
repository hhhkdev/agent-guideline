# Next.js API 연동 및 TanStack Query 가이드라인

## 1. API 함수 및 타입 작성 규칙

모든 API 호출은 `src/services/[domain]/` 하위에 DTO 인터페이스와 함께 작성합니다.

```typescript
// src/services/user/types.ts
export interface UserProfileDto {
  id: string;
  name: string;
  email: string;
  avatarUrl?: string;
}

export interface UpdateUserProfileRequest {
  name: string;
  avatarUrl?: string;
}
```

```typescript
// src/services/user/api.ts
import { apiClient } from '@/services/client';
import { UserProfileDto, UpdateUserProfileRequest } from './types';

export const userApi = {
  getProfile: async (): Promise<UserProfileDto> => {
    const { data } = await apiClient.get<UserProfileDto>('/v1/users/me');
    return data;
  },
  updateProfile: async (payload: UpdateUserProfileRequest): Promise<UserProfileDto> => {
    const { data } = await apiClient.patch<UserProfileDto>('/v1/users/me', payload);
    return data;
  }
};
```

---

## 2. TanStack Query 훅 및 캐시 키 관리

1. **Query Keys 팩토리 패턴 준수**: 문자열 하드코딩 금지.
```typescript
// src/services/user/queries.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { userApi } from './api';
import { UpdateUserProfileRequest } from './types';

export const userKeys = {
  all: ['users'] as const,
  profile: () => [...userKeys.all, 'profile'] as const,
};

export const useUserProfile = () => {
  return useQuery({
    queryKey: userKeys.profile(),
    queryFn: userApi.getProfile,
    staleTime: 1000 * 60 * 5, // 5분
  });
};

export const useUpdateUserProfile = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: UpdateUserProfileRequest) => userApi.updateProfile(payload),
    onSuccess: (updated) => {
      queryClient.setQueryData(userKeys.profile(), updated);
      queryClient.invalidateQueries({ queryKey: userKeys.profile() });
    },
  });
};
```
