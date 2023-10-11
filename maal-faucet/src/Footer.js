import "./Footer.css";

export default function FooterWithLogo() {
  return (
    <>
      <div className="faucet-container_footer">
        <div className="m-q-d-f j-c-s-b a-i-c">
          <div className="m-y-1">
            <img
              src="https://maalscan.io/images/MAALScan-3b6a4eb934bb59f3b26669ca9b58e270.png?vsn=d"
              className="w-5"
            />
          </div>
          <div className="d-f j-c-c a-i-c flex-wrap ">
            <a href="https://maalchain.com/" target="_blank">
              <div className="m-y-1 m-r-2">MaalChain</div>
            </a>
            <a href="https://docs.maalscan.io/" target="_blank">
              {" "}
              <div className="m-y-1 m-r-2">Document</div>
            </a>
            <a href="https://github.com/maalchain" target="_blank">
              {" "}
              <div className="m-y-1">Github</div>
            </a>
          </div>
        </div>
        <hr />
        <div className="t-a-c m-y-1">@ 2023 MaalChain</div>
      </div>{" "}
    </>
  );
}
