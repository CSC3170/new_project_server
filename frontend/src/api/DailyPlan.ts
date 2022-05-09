import { AuthContextType } from '../auth/AuthContext';
import { IDailyPlan } from '../model/DailyPlan';
import { IWord } from '../model/Word';

const queryDailyPlans = async (authContext: AuthContextType) => {
  const res = await fetch('/api/daily-plans', {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${authContext.token}`,
    },
  });
  if (!res.ok) {
    if (res.status == 401) {
      authContext.setToken(null);
    } else {
      throw new Error(res.statusText);
    }
  }
  return (await res.json()) as IDailyPlan[];
};

const queryDailyPlanWord = async (book_name: string, authContext: AuthContextType) => {
  const res = await fetch(`/api/daily-plan/${book_name}/word`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${authContext.token}`,
    },
  });
  if (!res.ok) {
    if (res.status == 401) {
      authContext.setToken(null);
    } else {
      throw new Error(res.statusText);
    }
  }
  return (await res.json()) as IWord;
};

const submitDailyPlanWord = async (book_name: string, authContext: AuthContextType) => {
  const res = await fetch(`/api/daily-plan/${book_name}/word`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${authContext.token}`,
    },
  });
  if (!res.ok) {
    if (res.status == 401) {
      authContext.setToken(null);
    } else {
      throw new Error(res.statusText);
    }
  }
  return (await res.json()) as IWord;
};

export { queryDailyPlans, queryDailyPlanWord, submitDailyPlanWord };
