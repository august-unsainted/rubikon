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

function setOption(i, select) {
  option = document.createElement('option');
  option.value = i.toString().padStart(2, '0');
  option.textContent = i.toString().padStart(2, '0');
  select.appendChild(option);
}

function setTime(start, end, replace = true) {
  function updateSelect(timeType) {
    const hourSelect = document.getElementById(`${timeType}-hour`);
    const minuteSelect = document.getElementById(`${timeType}-minute`);

    if (replace) {
      hourSelect.replaceChildren();
      minuteSelect.replaceChildren();
    }

    for (let i = start; i <= end; i++) {
      if (i != 10) {
        i == 24 ? (hour = 0) : (hour = i);
        setOption(hour, hourSelect);
      }
    }

    for (let i = 0; i < 60; i += 15) {
      setOption(i, minuteSelect);
    }
  }
  updateSelect('start');
  updateSelect('end');
}

function updateHoursOfWork() {
  const selectedDate = new Date(dateInput.value);
  formattedDateElement.textContent = getFormattedDate(selectedDate);
  weekday = selectedDate.getDay();

  if (weekday > 3 && weekday <= 5) {
    setTime(0, 9);
    setTime(17, 23, false);
  } else {
    weekday > 0 && weekday <= 3 ? setTime(17, 24) : setTime(0, 23);
  }
};

function updateDate() {
  dateInput.setAttribute('min', minDate);
  dateInput.value = minDate;
  formattedDateElement.textContent = getFormattedDate(new Date(dateInput.value));
  updateHoursOfWork();
};

updateDate();

dateInput.addEventListener('change', updateHoursOfWork);

const form = document.getElementById('form');
form.addEventListener('reset', () => {
  updateDate();
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
  values = {};
  inputs.concat(selects).forEach((field) => {
    values[field.id] = field.value;
  });

  values['date'] = document.getElementById('formattedDate').textContent;
  values['not_formatted_date'] = document.getElementById('date').value;
  const minDateObj = new Date(minDate);
  values['today'] = getFormattedDate(minDateObj);
  minDateObj.setDate(minDateObj.getDate() + 1)
  values['tomorrow'] = getFormattedDate(minDateObj);
  if (type) {
    values = await eel.get_primary_info(values)();
  } else {
    values = await eel.get_info(values)();
  }

  return values;
}

async function get_data(type = null) {
   values = await get_main_info(type)

   if (!type) {
    if (values['prepayment_info']) {
    document.getElementById('summary-prepayment-info').value =
      values['prepayment_info'];
  }

  if (values['goodbye_info']) {
    document.getElementById('summary-goodbye-info').value =
      values['goodbye_info'];
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
};

timeSelects = document.getElementsByClassName('time-select')

for (let i = 0; i < timeSelects.length; i++) {
  timeSelects[i].addEventListener('change', async () => {
    await updateTime('hours');
    get_data('primary');
  })
}

document.getElementById('hours').addEventListener('change', async () => {
  await updateTime();
  get_data('primary');
})

Array.from(document.getElementsByClassName('primary-field')).forEach((field) => {
  field.addEventListener('change', () => get_data('primary'))
});


function validateInput(input) {
  let value = input.value.replace(/[^а-яё]/gi, '');
  if (value.length > 0) {
    value = value.charAt(0).toUpperCase() + value.slice(1).toLowerCase();
  }
  input.value = value;
}

document.getElementById('btn-submit-to-google-sheets').onclick = async () => {
  values = await get_main_info();
  values['worker'] = document.getElementById('worker').value;
  values['source'] = document.getElementById('source').value;
  //  checkbox = document.getElementById('checkbox-payment-confirmed');
  //  values['checkbox-payment-confirmed'] = checkbox.checked;
  await eel.get_sheets(values);
};

document.querySelectorAll('.form-field__input').forEach((input) => {
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
