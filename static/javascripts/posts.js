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

const controlLimitBtn = () => {
  const minusBtn = document.getElementById('minus_button');
  const plusBtn = document.getElementById('plus_button');
  const limitElm = document.getElementById('rides_limit');

  minusBtn.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    let rides_limit = parseInt(document.getElementById('rides_limit').value);
    if (rides_limit > 1) {
      limitElm.value = rides_limit - 1;
    }
  });
  plusBtn.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    let rides_limit = parseInt(document.getElementById('rides_limit').value);
    limitElm.value = rides_limit + 1;
  });
};

const validatePostForm = () => {
  const departure = document.getElementById('departure').value;
  const destination = document.getElementById('destination').value;
  const dateTime = document.getElementById('datetimepicker').value;
  const rides_limit = document.getElementById('rides_limit').value;
  const updateBtn = document.getElementById('request_post_btn');

  if (!departure || !destination || !dateTime || !rides_limit) {
    updateBtn.setAttribute('disabled', true);
    updateBtn.classList.remove('bg-Primary');
    updateBtn.classList.add('bg-Low');
  } else {
    updateBtn.removeAttribute('disabled');
    updateBtn.classList.remove('bg-Low');
    updateBtn.classList.add('bg-Primary');
  }
};

document.addEventListener('DOMContentLoaded', () => {
  flatpickr('#datetimepicker', {
    enableTime: true,
    locale: 'ko',
    dateFormat: `Y년 m월 d일 (D) H:i`,
    defaultDate: new Date(),
  });

  spreadFilters();
});

document.addEventListener('DOMContentLoaded', () => {
  document
    .getElementById('control_buttons_div')
    .addEventListener('click', controlLimitBtn);
  document
    .getElementById('update_post_form')
    .addEventListener('input', validatePostForm);
});
