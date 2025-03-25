const dateInput = document.getElementById('date');
const today = new Date();
const year = today.getFullYear();
const month = String(today.getMonth() + 1).padStart(2, '0');
const day = String(today.getDate()).padStart(2, '0');
const minDate = `${year}-${month}-${day}`;
const formattedDateElement = document.getElementById('formattedDate');

function getFormattedDate(date) {
  const optionsDayMonth = { day: 'numeric', month: 'long' };
  const optionsWeekday = { weekday: 'long' };
  const dayMonth = date.toLocaleDateString('ru-RU', optionsDayMonth);
  const weekday = date.toLocaleDateString('ru-RU', optionsWeekday);
  const formattedDate = `${dayMonth} (${weekday})`;
  return formattedDate;
  //  formattedDateElement.textContent = formattedDate;
}

function fillTime() {
  function setOption(i, select) {
    option = document.createElement('option');
    option.value = i.toString().padStart(2, '0');
    option.textContent = i.toString().padStart(2, '0');
    select.append(option);
  }

  function updateSelect(timeType) {
    const $hourSelect = $(`#${timeType}-hour`);
    const $minuteSelect = $(`#${timeType}-minute`);

    for (let i = 1; i <= 24; i++) {
      if (i != 10) {
        i == 24 ? (hour = 0) : (hour = i);
        setOption(hour, $hourSelect);
      }
    }

    for (let i = 0; i < 60; i += 15) {
      setOption(i, $minuteSelect);
    }
  }

  updateSelect('start');
  updateSelect('end');
}

function setTime(start, end, reset = false, hide = true) {
  function updateSelect(timeType) {
    const hourSelect = document.getElementById(`${timeType}-hour`);
    const minuteSelect = document.getElementById(`${timeType}-minute`);

    for (let i = 1; i <= 24; i++) {
      i == 24 ? (hour = 0) : (hour = i);
      option = hourSelect.querySelector(
        `option[value="${hour.toString().padStart(2, '0')}"]`
      );
      if (i < start || i > end) {
        if (hide && option != null) option.setAttribute('hidden', '');
      } else {
        if (option != null) option.removeAttribute('hidden');
      }
    }

    const selectOption = (select) => {
      select
        .querySelector(`option[value="${select.value}"]`)
        .removeAttribute('selected');
      select
        .querySelector(`option[value="${start.toString().padStart(2, '0')}"]`)
        .setAttribute('selected', '');
    };

    if (reset) {
      selectOption(hourSelect);
      // selectOption(minuteSelect);
    }
  }

  updateSelect('start');
  updateSelect('end');
}

function updateHoursOfWork(reset = false) {
  const selectedDate = new Date(dateInput.value);
  formattedDateElement.textContent = getFormattedDate(selectedDate);
  let weekday = selectedDate.getDay();

  if (weekday == 5) {
    setTime(1, 9, reset);
    setTime(17, 24, reset, false);
  } else {
    weekday > 0 && weekday <= 4
      ? setTime(17, 24, reset)
      : setTime(1, 24, reset);
  }
}

function updateDate(reset = false) {
  dateInput.setAttribute('min', minDate);
  dateInput.setAttribute('value', minDate);
  dateInput.value = minDate;
  updateHoursOfWork(reset);
}

fillTime();
updateDate();

dateInput.addEventListener('change', updateHoursOfWork);

const form = document.getElementById('form');
form.addEventListener('reset', () => {
  updateDate(true);
});

async function update_end(startTime) {
  hours = document.getElementById('hours').value;
  end = await eel.update_end(startTime, hours)();
  end = end.split(':');
  document.getElementById('end-hour').value = end[0];
  document.getElementById('end-minute').value = end[1];
}

async function get_main_info(type = null) {
  inputs = Array.from(document.getElementsByTagName('input'));
  selects = Array.from(document.getElementsByTagName('select'));
  let values = {};
  inputs.concat(selects).forEach((field) => {
    values[field.id] = field.value;
  });
  values['already_was'] = document.getElementById(
    'checkbox-already-was'
  ).checked;
  values['date'] = document.getElementById('formattedDate').textContent;
  values['not_formatted_date'] = document.getElementById('date').value;
  const minDateObj = new Date(minDate);
  values['today'] = getFormattedDate(minDateObj);
  minDateObj.setDate(minDateObj.getDate() + 1);
  values['tomorrow'] = getFormattedDate(minDateObj);
  if (type) {
    values = await eel.get_primary_info(values)();
  } else {
    values = await eel.get_info(values)();
  }

  return values;
}

async function get_data(type = null) {
  values = await get_main_info(type);

  if (!type) {
    if (values['prepayment_info']) {
      document.getElementById('summary-prepayment-info').value =
        values['prepayment_info'];
    }

    if (values['goodbye_info']) {
      document.getElementById('summary-goodbye-info').value =
        values['goodbye_info'];
    } else {
      document.getElementById('summary-goodbye-info').value = '';
    }
  }

  results = document.getElementsByClassName('form-field__value');
  Array.from(results).forEach(
    (result) => (result.textContent = values[result.id])
  );
}

document.getElementById('btn-apply').onclick = () => get_data();

async function updateTime(type) {
  function getTime(prefix) {
    hour = document.getElementById(`${prefix}-hour`).value;
    minute = document.getElementById(`${prefix}-minute`).value;
    return `${hour}:${minute}`;
  }

  startTime = getTime('start');

  if (type == 'hours') {
    endTime = getTime('end');
    document.getElementById('hours').value = await eel.update_hours(
      startTime,
      endTime
    )();
  } else {
    await update_end(startTime);
  }
}

timeSelects = document.getElementsByClassName('time-select');

for (let i = 0; i < timeSelects.length; i++) {
  timeSelects[i].addEventListener('change', async () => {
    await updateTime('hours');
    get_data('primary');
  });
}

document.getElementById('hours').addEventListener('change', async () => {
  await updateTime();
  get_data('primary');
});

Array.from(document.getElementsByClassName('primary-field')).forEach(
  (field) => {
    field.addEventListener('change', () => {
      if (document.getElementById('hours').value) get_data('primary');
    });
  }
);

const nameInput = document.getElementById('name');
nameInput.addEventListener('input', () => {
  let value = nameInput.value.replace(/[^а-яё]/gi, '');
  if (value.length > 0) {
    value = value.charAt(0).toUpperCase() + value.slice(1).toLowerCase();
  }
  nameInput.value = value;
});

const phoneInput = document.getElementById('phone');
phoneInput.addEventListener('input', () => {
  let value = phoneInput.value.replace(/[^0-9]/g, '');
  if (value.length > 0) {
    value = '8' + value.slice(1);
  }
  phoneInput.value = value;
});

const clientsInput = document.getElementById('clients');
clientsInput.onchange = () => {
  const serviceOptions = document.getElementById('service').children;
  if (clientsInput.value > 2) {
    for (let i = 0; i <= 8; i++) {
      if (serviceOptions[i].value.startsWith('Киносвидание')) {
        serviceOptions[i].setAttribute('hidden', '');
        serviceOptions[i].removeAttribute('selected');
      } else serviceOptions[i].removeAttribute('hidden');
    }
    values = {
      3: 4,
      4: 5,
      7: 5,
      8: 7,
      10: 7,
      11: 8,
    };
    let room = values[clientsInput.value];
    if (room) {
      document
        .querySelector('#service option:checked')
        .removeAttribute('selected');
      serviceOptions[room].setAttribute('selected', '');
    }
    //        console.log(values[clientsInput.value], serviceOptions[values[clientsInput.value]])
    //        serviceOptions[values[clientsInput.value]].setAttribute('selected', '')
  } else {
    for (let i = 0; i <= 8; i++) {
      serviceOptions[i].value.startsWith('Киносвидание')
        ? serviceOptions[i].removeAttribute('hidden')
        : serviceOptions[i].setAttribute('hidden', '');
    }
    serviceOptions[4].removeAttribute('selected');
    serviceOptions[0].setAttribute('selected', '');
  }
};

document.getElementById('btn-submit-to-google-sheets').onclick = async () => {
  values = await get_main_info();
  values['worker'] = document.getElementById('worker').value;
  values['source'] = document.getElementById('source').value;
  //  checkbox = document.getElementById('checkbox-payment-confirmed');
  //  values['checkbox-payment-confirmed'] = checkbox.checked;
  await eel.get_sheets(values);
};

Array.from(document.getElementsByClassName('btn-copy')).forEach((button) => {
  button.onclick = () => {
    search_id = button.id.replace('btn-copy-', 'summary-');
    const field = document.getElementById(search_id);
    navigator.clipboard.writeText(field.value);
  };
});

let textareas = Array.from(document.querySelectorAll('.form-field__textarea'));
let inputs = Array.from(document.querySelectorAll('.form-field__input'));

inputs.concat(textareas).forEach((input) => {
  input.addEventListener('focus', function () {
    const parentField = this.closest('.form-field');
    parentField.classList.add('--focused');
  });

  input.addEventListener('blur', function () {
    const parentField = this.closest('.form-field');
    parentField.classList.remove('--focused');
  });
});

function t(i) {
  const tabs = document.querySelectorAll('.tabs__content-page');
  const buttons = document.querySelectorAll('.tabs__button');

  tabs.forEach((tab, j) => tab.classList.toggle('--open-tab', j == i));
  buttons.forEach((btn, j) => btn.classList.toggle('--active', j == i));
}
