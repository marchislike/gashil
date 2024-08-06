const handleFilterClick = (li) => {
  if (li.classList.contains('bg-Low text-Primary')) {
    li.classList.remove('bg-Low text-Primary');
    li.classList.add('bg-Primary text-white');
  } else {
    li.classList.remove('bg-Primary text-white');
    li.classList.add('bg-Low text-Primary');
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
};

document.addEventListener('DOMContentLoaded', () => {
  spreadFilters();
  document.getElementById('filters').addEventListener('click', (event) => {
    if (event.target.tagName === 'li') handleFilterClick(e.target);
  });
});
