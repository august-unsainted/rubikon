const today = new Date();
const year = today.getFullYear();
const month = String(today.getMonth() + 1).padStart(2, '0');
const day = String(today.getDate()).padStart(2, '0');
const minDate = `${year}-${month}-${day}`;

const dateInput = document.getElementById('date');
dateInput.setAttribute('min', minDate);

dateInput.value = minDate;

const formattedDateElement = document.getElementById('formattedDate');

function updateFormattedDate(date) {
  const optionsDayMonth = { day: 'numeric', month: 'long' };
  const optionsWeekday = { weekday: 'long' };
  const dayMonth = date.toLocaleDateString('ru-RU', optionsDayMonth);
  const weekday = date.toLocaleDateString('ru-RU', optionsWeekday);
  const formattedDate = `${dayMonth} (${weekday})`;
  formattedDateElement.textContent = formattedDate;
}

updateFormattedDate(new Date(dateInput.value));

dateInput.addEventListener('change', function () {
  const selectedDate = new Date(this.value);
  updateFormattedDate(selectedDate);
});

function set_time(i, select) {
  option = document.createElement('option');
  option.value = i.toString().padStart(2, '0');
  option.textContent = i.toString().padStart(2, '0');
  select.appendChild(option);
}

function populateTimeSelect(hourId, minuteId) {
  const hourSelect = document.getElementById(hourId);
  const minuteSelect = document.getElementById(minuteId);

  for (let i = 0; i <= 23; i++) {
    set_time(i, hourSelect);
  }

  for (let i = 0; i < 60; i += 15) {
    set_time(i, minuteSelect);
  }
}

populateTimeSelect('start-hour', 'start-minute');
populateTimeSelect('end-hour', 'end-minute');

async function update_end() {
  hours = document.getElementById('hours').value;
  end = await eel.update_end(startTime, hours)();
  end = end.split(':');
  document.getElementById('end-hour').value = end[0];
  document.getElementById('end-minute').value = end[1];
}

document.getElementById('apply-button').onclick = async () => {
  inputs = Array.from(document.getElementsByTagName('input'));
  selects = Array.from(document.getElementsByTagName('select'));
  values = {};
  inputs.concat(selects).forEach((field) => {
    values[field.id] = field.value;
  });

  values['date'] = document.getElementById('formattedDate').textContent;
  values = await eel.get_info(values)();

  document.getElementById('hours').value = values['hours'];
  await update_end();

  if (values['prepayment_info']) {
    document.getElementById('prepayment_info').value =
      values['prepayment_info'];
  }
};

Array.from(document.getElementsByClassName('update_button')).forEach(
  (button) => {
    button.onclick = async () => {
      function getTime(prefix) {
        hour = document.getElementById(`${prefix}-hour`).value;
        minute = document.getElementById(`${prefix}-minute`).value;
        return `${hour}:${minute}`;
      }

      startTime = getTime('start');

      if (button.id == 'update_hours') {
        endTime = getTime('end');
        document.getElementById('hours').value = await eel.update_hours(
          startTime,
          endTime
        )();
      } else {
        await update_end();
      }
    };
  }
);

document.getElementById('copy-button').onclick = () => {
  const textarea = document.getElementById('prepayment_info');
  navigator.clipboard.writeText(textarea.value);
};

function validateInput(input) {
  // 1. Оставляем только русские буквы (в нижнем регистре)
  let value = input.value.replace(/[^а-яё]/gi, '');

  // 2. Делаем первую букву заглавной, если строка не пустая
  if (value.length > 0) {
      value = value.charAt(0).toUpperCase() + value.slice(1).toLowerCase();
  }

  // 3. Обновляем значение поля ввода
  input.value = value;
}
