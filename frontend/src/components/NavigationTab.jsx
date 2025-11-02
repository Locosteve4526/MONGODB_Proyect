import CustomButton from "./CustomButton";
import "../static/NavigationTab.css";

function NavigationTab({ selection, setSelection }) {
  const isUserSelected = selection == 1 ? true : false;
  const isAuthorSelected = selection == 2 ? true : false;
  const isBookSelected = selection == 3 ? true : false;
  const isEditionSelected = selection == 4 ? true : false;
  const isCopySelected = selection == 5 ? true : false;
  const isLoanSelected = selection == 6 ? true : false;

  let selectUser = () => {
    setSelection(1);
    console.log(selection);
  };
  let selectAuthor = () => {
    setSelection(2);
    console.log(selection);
  };
  let selectBook = () => {
    setSelection(3);
    console.log(selection);
  };
  let selectEdition = () => {
    setSelection(4);
    console.log(selection);
  };
  let selectCopy = () => {
    setSelection(5);
    console.log(selection);
  };
  let selectLoan = () => {
    setSelection(6);
    console.log(selection);
  };

  return (
    <ul>
      <li>
        <CustomButton
          label={"Usuario"}
          onClick={selectUser}
          selected={isUserSelected}
        />
      </li>
      <li>
        <CustomButton
          label={"Autor"}
          onClick={selectAuthor}
          selected={isAuthorSelected}
        />
      </li>
      <li>
        <CustomButton
          label={"Libro"}
          onClick={selectBook}
          selected={isBookSelected}
        />
      </li>
      <li>
        <CustomButton
          label={"Edición"}
          onClick={selectEdition}
          selected={isEditionSelected}
        />
      </li>
      <li>
        <CustomButton
          label={"Copia"}
          onClick={selectCopy}
          selected={isCopySelected}
        />
      </li>
      <li>
        <CustomButton
          label={"Prestamo"}
          onClick={selectLoan}
          selected={isLoanSelected}
        />
      </li>
    </ul>
  );
}

export default NavigationTab;
