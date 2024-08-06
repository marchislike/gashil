const handleFilterClick = (li) => {
  if (li.classList.contains('bg-gray-100')) {
    li.classList.remove('bg-gray-100', 'text-gray-400');
    li.classList.add('bg-Low', 'text-Strong');
  } else {
    li.classList.remove('bg-Low', 'text-Strong');
    li.classList.add('bg-gray-100', 'text-gray-400');
  }
};

const spreadFilters = () => {
  const ul = document.getElementById('filters');
  const selectedFilters = [
    '문지 기숙사',
    '대전역',
    '다이소',
    '카이스트 본원',
    '코치님 연구실',
  ];
  selectedFilters.forEach((filter) => {
    const list = `<li
        id=${filter}
        class="px-[18px] py-[5px] rounded-full w-fit flex-shrink-0 cursor-pointer font-semibold text-[14px] bg-gray-100 text-gray-400"
        onClick='handleFilterClick'
      >
        ${filter}
      </li>`;

    ul.insertAdjacentHTML('beforeend', list);
  });
  ul.addEventListener('click', (event) => {
    if (event.target.tagName === 'LI') handleFilterClick(event.target);
  });
};

const getDateTime = () => {
  const time = document.getElementById('time');

  const date = new Date();
  const hour = date.getHours();
  const min = date.getMinutes();

  time.setAttribute('value', `${hour}:${min}`);
};

document.addEventListener('DOMContentLoaded', () => {
  getDateTime();
  spreadFilters();
});
