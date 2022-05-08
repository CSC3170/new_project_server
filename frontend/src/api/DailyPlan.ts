import { AuthContextType } from '../auth/AuthContext';
import { DailyPlan } from '../model/DailyPlan';
import { WordType } from '../model/Word';

const queryDailyPlans = async (authContext: AuthContextType) => {
  const res = await fetch('/api/daily-plans', {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${authContext.token}`,
    },
  });
  if (!res.ok) {
    if (res.status == 400) {
      authContext.setToken(null);
    } else {
      throw new Error(res.statusText);
    }
  }
  return (await res.json()) as DailyPlan[];
};

const queryDailyPlanWord = async (book_name: string, authContext: AuthContextType) => {
  const res = await fetch(`/api/daily-plan/${book_name}/word`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${authContext.token}`,
    },
  });
  if (!res.ok) {
    if (res.status == 400) {
      authContext.setToken(null);
    } else {
      throw new Error(res.statusText);
    }
  }
  return (await res.json()) as WordType;
};

const submitDailyPlanWord = async (book_name: string, authContext: AuthContextType) => {
  const res = await fetch(`/api/daily-plan/${book_name}/word`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${authContext.token}`,
    },
  });
  if (!res.ok) {
    if (res.status == 400) {
      authContext.setToken(null);
    } else {
      throw new Error(res.statusText);
    }
  }
  return (await res.json()) as WordType;
};

export { queryDailyPlans, queryDailyPlanWord, submitDailyPlanWord };
