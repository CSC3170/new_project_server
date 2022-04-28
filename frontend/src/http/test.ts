import fetch from 'isomorphic-fetch';
import _ from 'lodash';

interface TestResponce {
  data: string;
}

const test = async (id: number): Promise<TestResponce> => {
  return fetch(`/api/test/${_.toString(id)}`).then((res) => {
    return res.json();
  });
};

export { test };
